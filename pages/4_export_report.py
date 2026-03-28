import streamlit as st
import pandas as pd
import json, io
from datetime import datetime

st.set_page_config(layout="wide")

IS_DARK  = st.get_option("theme.base") == "dark"
TEXT_CLR = "#f5e6f0" if IS_DARK else "#1a0030"
SUB_CLR  = "#d4cce8" if IS_DARK else "#7a3058"
CARD_BG  = "rgba(40, 15, 35, 0.85)" if IS_DARK else "rgba(255,255,255,0.9)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');
html, body {{ font-family: 'Quicksand', sans-serif !important; }}
.stMarkdown p, .stMarkdown span, [data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"] p, button[data-baseweb="tab"],
.stSelectbox label, .stSlider label, .stRadio label,
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {{
    font-family: 'Quicksand', sans-serif !important;
}}
.main .block-container {{
    padding-top: 2.5rem !important;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}}
.hero {{
    background: {"linear-gradient(120deg, #1a0030 0%, #3d0060 55%, #FF007F 100%)" if IS_DARK else "linear-gradient(120deg, #6b21a8 0%, #9333ea 55%, #FF007F 100%)"};
    border-radius: 16px; padding: 2rem 2.5rem 1.7rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}}
.hero::before {{
    content: ""; position: absolute; right: -50px; top: -50px;
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,0,127,.28) 0%, transparent 70%);
}}
.hero h1 {{ font-weight:700 !important; font-size:2rem !important; color:#fff !important; margin:0 0 .3rem !important; }}
.hero p  {{ color:rgba(255,255,255,.6) !important; margin:0 !important; font-size:.9rem !important; }}
.badge {{
    display:inline-block; background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.22);
    border-radius:20px; padding:2px 12px; font-size:.68rem; color:#ffb3d9;
    letter-spacing:1.2px; text-transform:uppercase; margin-bottom:.5rem;
}}
.metric-row {{ display:flex; gap:12px; margin-bottom:1.8rem; flex-wrap:wrap; }}
.mc {{ flex:1; min-width:100px; border-radius:12px; padding:.85rem 1rem; text-align:center;
       border:1.5px solid rgba(255,94,163,.3); background:{CARD_BG}; }}
.mc-val {{ font-family:'JetBrains Mono',monospace; font-size:1.5rem; font-weight:600; color:#FF5EA3; }}
.mc-lbl {{ font-size:.65rem; color:{SUB_CLR}; text-transform:uppercase; letter-spacing:.9px; margin-top:3px; font-weight:700; }}
.sec-title {{
    font-weight:700 !important; font-size:1.1rem !important; color:#FF5EA3 !important;
    display:block; margin:1.4rem 0 .8rem; padding-bottom:.3rem;
    border-bottom:2px solid rgba(255,94,163,.3);
}}
.log-step {{
    padding:.75rem 1rem; border-radius:10px; margin-bottom:8px;
    border:1px solid rgba(255,94,163,.25); background:{CARD_BG};
}}
.log-op   {{ font-weight:700; font-size:.88rem; color:{TEXT_CLR}; }}
.log-meta {{ font-size:.76rem; color:{SUB_CLR}; margin-top:3px; line-height:1.5; }}
.report-box {{
    background:{"#1a0020" if IS_DARK else "#fff0f7"}; border:1.5px solid rgba(255,94,163,.3);
    border-radius:12px; padding:1.1rem 1.3rem; font-family:'JetBrains Mono',monospace;
    font-size:.76rem; line-height:1.7; color:{TEXT_CLR}; white-space:pre-wrap;
    max-height: 500px; overflow-y: auto;
}}
.stDownloadButton > button {{
    background:linear-gradient(135deg,#FF007F,#c0006a) !important;
    color:#fff !important; border:none !important; border-radius:8px !important; font-weight:600 !important;
}}
.stButton > button {{
    border:1.5px solid #FF007F !important; color:#FF007F !important;
    background:transparent !important; border-radius:8px !important; font-weight:600 !important;
}}
.stButton > button:hover {{ background:rgba(255,0,127,.1) !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom:3px solid #FF007F !important; color:#FF007F !important; font-weight:700 !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.markdown('<div class="hero"><div class="badge">Page D</div>'
                '<h1>Export &amp; Report</h1><p>Upload a dataset first.</p></div>', unsafe_allow_html=True)
    st.stop()

df   = st.session_state["df"]
orig = st.session_state.get("original_df", df)
log  = st.session_state.get("log", [])
now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_step_fields(step):
    op     = (step.get("Action") or step.get("operation") or step.get("action")
              or step.get("step") or step.get("type") or step.get("name") or "Unknown")
    detail = (step.get("Details") or step.get("parameters") or step.get("params") or "")
    cols   = (step.get("columns") or step.get("affected_columns") or step.get("column") or "")
    ts     = (step.get("Time") or step.get("timestamp") or "")
    return op, detail, cols, ts

def build_report_text(df, orig, log, now):
    """Build the professional report as a string."""
    num_c = df.select_dtypes(include="number").columns.tolist()
    cat_c = df.select_dtypes(include=["object","category"]).columns.tolist()
    miss_by_col = df.isnull().sum()
    miss_by_col = miss_by_col[miss_by_col > 0]
    W = 60

    def section(title):
        return f"\n{'─' * W}\n  {title}\n{'─' * W}"

    parts = [
        "╔" + "═" * (W-2) + "╗",
        "║" + "  DATACRAFT — DATA TRANSFORMATION REPORT".center(W-2) + "║",
        "╚" + "═" * (W-2) + "╝",
        "",
        f"  Generated       : {now}",
        f"  Report Version  : 1.0",
        "",
        section("1. DATASET SUMMARY"),
        f"  Original shape  : {len(orig):,} rows  x  {len(orig.columns)} columns",
        f"  Cleaned shape   : {len(df):,} rows  x  {len(df.columns)} columns",
        f"  Rows removed    : {len(orig) - len(df):,}",
        f"  Columns removed : {len(orig.columns) - len(df.columns)}",
        f"  Missing values  : {int(df.isnull().sum().sum()):,}",
        f"  Duplicates      : {int(df.duplicated().sum()):,}",
        "",
        section("2. COLUMN OVERVIEW"),
        f"  Numeric columns ({len(num_c)})     : {', '.join(num_c) if num_c else 'None'}",
        f"  Categorical columns ({len(cat_c)}) : {', '.join(cat_c) if cat_c else 'None'}",
    ]

    if not miss_by_col.empty:
        parts += ["", "  Remaining missing values by column:"]
        for col, cnt in miss_by_col.items():
            pct = cnt / len(df) * 100
            parts.append(f"    - {col:<25} {cnt:>5} missing  ({pct:.1f}%)")

    parts += ["", section("3. TRANSFORMATION STEPS")]
    if log:
        for i, s in enumerate(log):
            op, detail, cols, ts = get_step_fields(s)
            c_str = ", ".join(cols) if isinstance(cols, list) else str(cols)
            d_str = json.dumps(detail, default=str) if isinstance(detail, dict) else str(detail)
            parts += [
                f"  Step {i+1:02d}",
                f"    Action    : {op}",
                f"    Columns   : {c_str if c_str else '-'}",
                f"    Details   : {d_str if d_str and d_str not in ['{}','None',''] else '-'}",
                f"    Timestamp : {ts if ts else '-'}",
                "",
            ]
    else:
        parts.append("  No transformations recorded.")

    parts += [section("4. COLUMN STATISTICS")]
    for col in df.columns:
        dtype   = str(df[col].dtype)
        missing = int(df[col].isnull().sum())
        unique  = int(df[col].nunique())
        if pd.api.types.is_numeric_dtype(df[col]):
            mn = df[col].min(); mx = df[col].max(); mean = df[col].mean()
            parts.append(f"  {col:<22} [{dtype:<8}]  missing={missing}  unique={unique}  min={mn:.2f}  max={mx:.2f}  mean={mean:.2f}")
        else:
            top = df[col].value_counts().index[0] if not df[col].dropna().empty else "-"
            parts.append(f"  {col:<22} [{dtype:<8}]  missing={missing}  unique={unique}  top='{top}'")

    parts += ["", "╔" + "═"*(W-2) + "╗",
              "║" + "  END OF REPORT".center(W-2) + "║",
              "╚" + "═"*(W-2) + "╝"]
    return "\n".join(parts)


def build_report_excel(df, orig, log, now):
    """Build a multi-sheet Excel report."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        # Sheet 1: Summary
        summary = pd.DataFrame([
            ["Generated",       now],
            ["Original shape",  f"{len(orig)} rows x {len(orig.columns)} cols"],
            ["Cleaned shape",   f"{len(df)} rows x {len(df.columns)} cols"],
            ["Rows removed",    len(orig) - len(df)],
            ["Missing values",  int(df.isnull().sum().sum())],
            ["Duplicates",      int(df.duplicated().sum())],
            ["Steps applied",   len(log)],
        ], columns=["Metric", "Value"])
        summary.to_excel(writer, sheet_name="Summary", index=False)

        # Sheet 2: Transformation Log
        if log:
            rows = []
            for i, s in enumerate(log):
                op, detail, cols, ts = get_step_fields(s)
                rows.append({"Step": i+1, "Action": op,
                             "Columns": ", ".join(cols) if isinstance(cols, list) else str(cols),
                             "Details": detail, "Timestamp": ts})
            pd.DataFrame(rows).to_excel(writer, sheet_name="Transformation Log", index=False)

        # Sheet 3: Column Stats
        stat_rows = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            row = {"Column": col, "Type": dtype,
                   "Missing": int(df[col].isnull().sum()),
                   "Missing %": round(df[col].isnull().mean()*100, 2),
                   "Unique": int(df[col].nunique())}
            if pd.api.types.is_numeric_dtype(df[col]):
                row.update({"Min": df[col].min(), "Max": df[col].max(), "Mean": round(df[col].mean(), 4)})
            else:
                top = df[col].value_counts().index[0] if not df[col].dropna().empty else "-"
                row["Top Value"] = top
            stat_rows.append(row)
        pd.DataFrame(stat_rows).to_excel(writer, sheet_name="Column Statistics", index=False)

        # Sheet 4: Cleaned Data
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)

    return buf.getvalue()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="badge">Page D · Export &amp; Report</div>
  <h1>Export &amp; Report</h1>
  <p>Download your cleaned dataset, transformation log, JSON recipe, and full report.</p>
</div>
<div class="metric-row">
  <div class="mc"><div class="mc-val">{len(df):,}</div><div class="mc-lbl">Rows</div></div>
  <div class="mc"><div class="mc-val">{len(df.columns)}</div><div class="mc-lbl">Columns</div></div>
  <div class="mc"><div class="mc-val">{int(df.isnull().sum().sum()):,}</div><div class="mc-lbl">Missing</div></div>
  <div class="mc"><div class="mc-val">{len(log)}</div><div class="mc-lbl">Steps Applied</div></div>
  <div class="mc"><div class="mc-val">{len(orig)-len(df):,}</div><div class="mc-lbl">Rows Removed</div></div>
</div>
""", unsafe_allow_html=True)

tab_prev, tab_log, tab_dl = st.tabs(["Preview", "Transformation Log", "Downloads"])

# ══ Preview ═══════════════════════════════════════════════════════════════════
with tab_prev:
    st.markdown('<span class="sec-title">Final Dataset</span>', unsafe_allow_html=True)
    n = st.slider("Rows to show", 5, min(200, len(df)), 20)
    st.dataframe(df.head(n), use_container_width=True)
    if len(orig) != len(df) or len(orig.columns) != len(df.columns):
        st.markdown('<span class="sec-title">Before vs After</span>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Original Rows", f"{len(orig):,}")
        c2.metric("Cleaned Rows",  f"{len(df):,}",        delta=f"{len(df)-len(orig):+,}")
        c3.metric("Original Cols", len(orig.columns))
        c4.metric("Cleaned Cols",  len(df.columns),       delta=f"{len(df.columns)-len(orig.columns):+,}")

# ══ Transformation Log ════════════════════════════════════════════════════════
with tab_log:
    st.markdown('<span class="sec-title">Transformation Log</span>', unsafe_allow_html=True)
    if not log:
        st.info("No transformations recorded. Apply cleaning steps on the Cleaning page.")
    else:
        st.caption(f"{len(log)} step(s) applied in this session.")
        for i, step in enumerate(log):
            op, detail, cols, ts = get_step_fields(step)
            c_str = ", ".join(cols) if isinstance(cols, list) else str(cols)
            d_str = json.dumps(detail, default=str) if isinstance(detail, dict) else str(detail)
            st.markdown(f"""
            <div class="log-step">
              <div class="log-op">#{i+1} &nbsp; {op}</div>
              <div class="log-meta">
                {"Columns: <b>" + c_str + "</b><br>" if c_str else ""}
                {"Details: " + d_str if d_str and d_str not in ["{}","None",""] else ""}
                {"<br><span style='opacity:.6;font-size:.7rem'>" + ts + "</span>" if ts else ""}
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        ca, cb = st.columns(2)
        with ca:
            if st.button("Undo Last Step"):
                st.session_state["log"].pop(); st.rerun()
        with cb:
            if st.button("Reset All Transformations"):
                st.session_state["df"]  = st.session_state.get("original_df", df).copy()
                st.session_state["log"] = []; st.rerun()

# ══ Downloads ═════════════════════════════════════════════════════════════════
with tab_dl:
    # ── Dataset exports ───────────────────────────────────────────────────────
    st.markdown('<span class="sec-title">Cleaned Dataset</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.download_button("Download CSV",
            df.to_csv(index=False).encode(), "cleaned_data.csv", "text/csv", key="dl_csv")
    with cb:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w: df.to_excel(w, index=False)
        st.download_button("Download Excel", buf.getvalue(), "cleaned_data.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_xlsx")

    # ── Recipe exports ────────────────────────────────────────────────────────
    st.markdown('<span class="sec-title">Pipeline Recipe</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    recipe = {
        "meta": {"title": "DataCraft Transformation Recipe", "generated": now,
                 "original_shape": {"rows": len(orig), "columns": len(orig.columns)},
                 "final_shape":    {"rows": len(df),   "columns": len(df.columns)},
                 "rows_removed": len(orig)-len(df), "steps_total": len(log)},
        "dataset": {"columns": list(df.columns),
                    "numeric_cols": df.select_dtypes(include="number").columns.tolist(),
                    "categorical_cols": df.select_dtypes(include=["object","category"]).columns.tolist()},
        "steps": [{"step": i+1, "action": get_step_fields(s)[0], "details": get_step_fields(s)[1],
                   "columns": get_step_fields(s)[2], "timestamp": get_step_fields(s)[3]}
                  for i, s in enumerate(log)],
    }
    with ca:
        st.download_button("Download JSON Recipe",
            json.dumps(recipe, indent=2, default=str).encode(),
            "recipe.json", "application/json", key="dl_recipe")

    def make_script(log):
        lines = ["# DataCraft — Auto-Generated Transformation Pipeline",
                 f"# Generated: {now}", "import pandas as pd", "import numpy as np", "",
                 "df = pd.read_csv('your_data.csv')", ""]
        for i, s in enumerate(log):
            op, detail, cols, ts = get_step_fields(s)
            lines += [f"# Step {i+1}: {op}", f"# Columns : {cols}",
                      f"# Details : {detail}", f"# Time    : {ts}", "# TODO: implement\n"]
        lines.append("df.to_csv('cleaned_data.csv', index=False)")
        return "\n".join(lines)

    with cb:
        st.download_button("Download Python Script",
            make_script(log).encode(), "pipeline.py", "text/plain", key="dl_py")

    # ── Transformation Report — multiple formats ───────────────────────────────
    st.markdown('<span class="sec-title">Transformation Report</span>', unsafe_allow_html=True)
    st.caption("Download the full transformation report in your preferred format.")

    report_text = build_report_text(df, orig, log, now)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.download_button("Download TXT",
            report_text.encode(), "report.txt", "text/plain", key="dl_txt")
    with c2:
        if log:
            rows = []
            for i, s in enumerate(log):
                op, detail, cols, ts = get_step_fields(s)
                rows.append({"Step": i+1, "Action": op,
                             "Columns": ", ".join(cols) if isinstance(cols, list) else str(cols),
                             "Details": detail, "Timestamp": ts})
            st.download_button("Download Log CSV",
                pd.DataFrame(rows).to_csv(index=False).encode(),
                "transformation_log.csv", "text/csv", key="dl_log")
        else:
            st.caption("No log yet.")
    with c3:
        try:
            excel_report = build_report_excel(df, orig, log, now)
            st.download_button("Download Excel Report", excel_report,
                "report.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_excel_report")
        except Exception as e:
            st.caption(f"Excel error: {e}")
    
    # ── Report preview ────────────────────────────────────────────────────────
    st.markdown('<span class="sec-title">Report Preview</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)

st.markdown("---")
if st.button("Reset Entire App"):
    st.session_state.clear(); st.rerun()
