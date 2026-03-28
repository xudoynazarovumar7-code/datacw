import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler

st.set_page_config(layout="wide")

# ── Theme ─────────────────────────────────────────────────────────────────────
IS_DARK  = st.get_option("theme.base") == "dark"
TEXT_CLR = "#f5f0ff" if IS_DARK else "#1a0030"
SUB_CLR  = "#d4cce8" if IS_DARK else "#5a4a7a"
CARD_BG  = "rgba(40, 15, 35, 0.85)" if IS_DARK else "rgba(255,255,255,0.9)"
BORD_CLR = "rgba(255,94,163,0.3)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

html, body {{ font-family: 'Quicksand', sans-serif !important; }}
.stMarkdown p, .stMarkdown span,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stCaptionContainer"] p,
[data-testid="metric-container"] p,
[data-testid="metric-container"] div,
button[data-baseweb="tab"],
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stNumberInput label,
.stRadio label, .stCheckbox label,
[data-testid="stExpander"] summary p,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {{
    font-family: 'Quicksand', sans-serif !important;
}}

.main .block-container {{
    padding-top: 2.5rem !important;
    max-width: 1200px;
    position: relative;
    z-index: 1;
}}

/* ── Hero ── */
.clean-hero {{
    background: {"linear-gradient(120deg, #1a0030 0%, #3d0060 55%, #FF007F 100%)" if IS_DARK else "linear-gradient(120deg, #6b21a8 0%, #9333ea 55%, #FF007F 100%)"};
    border-radius: 16px; padding: 2rem 2.5rem 1.7rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}}
.clean-hero::before {{
    content: ""; position: absolute; right: -50px; top: -50px;
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,0,127,.28) 0%, transparent 70%);
}}
.clean-hero h1 {{
    font-weight: 700 !important; font-size: 2rem !important;
    color: #fff !important; margin: 0 0 .35rem !important;
}}
.clean-hero p {{ color: rgba(255,255,255,.65) !important; margin: 0 !important; font-size: .92rem !important; }}
.cl-badge {{
    display: inline-block; background: rgba(255,255,255,.1);
    border: 1px solid rgba(255,255,255,.22); border-radius: 20px;
    padding: 2px 12px; font-size: .68rem; color: #ffb3d9;
    letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: .5rem;
}}

/* ── Stat bar ── */
.stat-bar {{ display: flex; gap: 12px; margin-bottom: 1.6rem; flex-wrap: wrap; }}
.sb {{
    flex: 1; min-width: 100px; border-radius: 12px;
    padding: .75rem 1rem; text-align: center;
    border: 1.5px solid {BORD_CLR}; background: {CARD_BG};
}}
.sb-val {{ font-family: 'JetBrains Mono', monospace !important; font-size: 1.35rem; font-weight: 600; color: #FF5EA3; }}
.sb-lbl {{ font-size: .62rem; color: {SUB_CLR} !important; text-transform: uppercase; letter-spacing: .9px; margin-top: 2px; font-weight: 700; }}

/* ── Panel ── */
.op-panel {{
    border: 1.5px solid {BORD_CLR}; border-radius: 14px;
    padding: 1.2rem 1.4rem; background: {CARD_BG};
    backdrop-filter: blur(6px); margin-bottom: 1rem;
}}
.op-label {{
    font-size: .68rem; font-weight: 700; letter-spacing: 1.4px;
    text-transform: uppercase; color: #FF5EA3; margin-bottom: .25rem;
}}
.op-title {{
    font-weight: 700; font-size: 1.1rem; color: {TEXT_CLR}; margin: 0 0 .1rem;
}}
.op-hint {{
    font-size: .8rem; color: {SUB_CLR} !important; line-height: 1.6; margin-top: .4rem;
}}
.op-hint strong {{ color: #FF5EA3 !important; }}

/* ── Section title ── */
.sec-title {{
    font-weight: 700; font-size: 1rem; color: {TEXT_CLR};
    margin: 1.2rem 0 .6rem; padding-bottom: .25rem;
    border-bottom: 2px solid rgba(255,94,163,.3); display: block;
}}

/* ── Buttons ── */
.stButton > button {{
    border: 1.5px solid #FF007F !important; color: #FF007F !important;
    background: transparent !important; border-radius: 8px !important;
    font-weight: 600 !important; transition: all .2s !important;
}}
.stButton > button:hover {{ background: rgba(255,0,127,.1) !important; }}

/* ── Tab active ── */
button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom: 3px solid #FF007F !important;
    color: #FF007F !important; font-weight: 700 !important;
}}

/* ── Log entry ── */
.log-entry {{
    font-size: .78rem; padding: .35rem .7rem; border-radius: 8px;
    background: rgba(255,94,163,.08); border-left: 3px solid #FF5EA3;
    margin-bottom: .3rem; color: {TEXT_CLR};
}}
</style>
""", unsafe_allow_html=True)

# ── Session safety ────────────────────────────────────────────────────────────
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("No dataset loaded. Please go to **Upload & Overview** first.")
    st.stop()

if "log" not in st.session_state:
    st.session_state["log"] = []

# ── Helper: log action ────────────────────────────────────────────────────────
def log_action(action: str, detail: str):
    st.session_state["log"].append({"Action": action, "Detail": detail})

# ── Helper: column type detection ────────────────────────────────────────────
def col_type(df, c):
    if pd.api.types.is_numeric_dtype(df[c]):    return "numeric"
    if pd.api.types.is_datetime64_any_dtype(df[c]): return "datetime"
    return "categorical"

def get_col_types(df, cols):
    return {c: col_type(df, c) for c in cols}

def fill_methods_for(col_types):
    types = set(col_types.values())
    if types == {"numeric"}:
        return ["mean", "median", "mode", "constant", "ffill", "bfill"]
    if types == {"categorical"}:
        return ["mode", "constant", "ffill", "bfill"]
    if types == {"datetime"}:
        return ["constant", "ffill", "bfill"]
    return ["mode", "constant", "ffill", "bfill"]

# ── Live stats bar ────────────────────────────────────────────────────────────
def stats_bar():
    df = st.session_state["df"]
    orig = st.session_state.get("original_df", df)
    missing = int(df.isnull().sum().sum())
    dupes   = int(df.duplicated().sum())
    st.markdown(f"""
    <div class="stat-bar">
      <div class="sb"><div class="sb-val">{df.shape[0]:,}</div><div class="sb-lbl">Rows</div></div>
      <div class="sb"><div class="sb-val">{df.shape[1]}</div><div class="sb-lbl">Columns</div></div>
      <div class="sb"><div class="sb-val">{missing:,}</div><div class="sb-lbl">Missing</div></div>
      <div class="sb"><div class="sb-val">{dupes:,}</div><div class="sb-lbl">Duplicates</div></div>
      <div class="sb"><div class="sb-val">{len(st.session_state['log'])}</div><div class="sb-lbl">Steps Applied</div></div>
      <div class="sb"><div class="sb-val">{orig.shape[0] - df.shape[0]:,}</div><div class="sb-lbl">Rows Removed</div></div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="clean-hero">
  <div class="cl-badge">Page B · Cleaning Studio</div>
  <h1>🧹 Cleaning &amp; Preparation Studio</h1>
  <p>Handle missing values, remove duplicates, fix types, encode categories, treat outliers, and scale — all in one place.</p>
</div>
""", unsafe_allow_html=True)

stats_bar()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Missing Values",
    "Duplicates",
    "Data Types",
    "Categorical",
    "Numeric / Outliers",
    "Scaling",
    "Columns",
    "Validation",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — MISSING VALUES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    df = st.session_state["df"]
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Handle Missing Values</div></div>', unsafe_allow_html=True)

        sel_cols = st.multiselect("Select columns", df.columns, key="mv_cols")
        action   = st.segmented_control("Action", ["Drop Rows", "Drop Columns by %", "Fill"], key="mv_action")

        method = value = threshold = dt_fmt = None

        if action == "Fill" and sel_cols:
            ctypes  = get_col_types(df, sel_cols)
            methods = fill_methods_for(ctypes)
            method  = st.segmented_control("Fill method", methods, key="mv_method")
            if method == "constant":
                all_num = all(t == "numeric" for t in ctypes.values())
                all_dt  = all(t == "datetime" for t in ctypes.values())
                if all_num:
                    value = st.number_input("Constant value", key="mv_const_num")
                elif all_dt:
                    value = st.text_input("Constant datetime value", key="mv_const_dt")
                    dt_fmt = st.text_input("Format (e.g. %Y-%m-%d)", key="mv_dt_fmt")
                else:
                    value = st.text_input("Constant value", key="mv_const_str")

        if action == "Drop Columns by %":
            threshold = st.number_input("Drop columns with missing > (%)", 0.0, 100.0, 50.0, key="mv_thresh")

        if st.button("Apply", key="mv_apply"):
            df_new = st.session_state["df"].copy()
            before_r, before_c = df_new.shape

            try:
                if action == "Drop Rows":
                    if not sel_cols:
                        st.warning("Select at least one column.")
                    else:
                        df_new = df_new.dropna(subset=sel_cols)
                        log_action("Drop Rows (missing)", f"cols={sel_cols}")

                elif action == "Drop Columns by %":
                    pct    = (df_new.isnull().sum() / len(df_new)) * 100
                    to_drop = pct[pct > threshold].index.tolist()
                    df_new  = df_new.drop(columns=to_drop)
                    log_action("Drop Columns by %", f"threshold={threshold}%, dropped={to_drop}")

                elif action == "Fill":
                    if not sel_cols:
                        st.warning("Select at least one column.")
                    elif method is None:
                        st.warning("Choose a fill method.")
                    else:
                        for c in sel_cols:
                            if method == "mean":
                                df_new[c] = df_new[c].fillna(df_new[c].mean())
                            elif method == "median":
                                df_new[c] = df_new[c].fillna(df_new[c].median())
                            elif method in ("mode", "most_frequent"):
                                m_ = df_new[c].mode()
                                if len(m_): df_new[c] = df_new[c].fillna(m_[0])
                            elif method == "constant":
                                if pd.api.types.is_datetime64_any_dtype(df_new[c]):
                                    parsed = pd.to_datetime(value, format=dt_fmt or None, errors="coerce")
                                    if pd.isna(parsed): st.error(f"{c}: invalid datetime"); st.stop()
                                    df_new[c] = df_new[c].fillna(parsed)
                                else:
                                    fill_val = float(value) if pd.api.types.is_numeric_dtype(df_new[c]) else value
                                    df_new[c] = df_new[c].fillna(fill_val)
                            elif method == "ffill":
                                df_new[c] = df_new[c].ffill()
                            elif method == "bfill":
                                df_new[c] = df_new[c].bfill()
                        log_action("Fill Missing", f"method={method}, cols={sel_cols}")

                st.session_state["df"] = df_new
                after_r, after_c = df_new.shape
                st.success("✅ Applied successfully")
                m1, m2, m3 = st.columns(3)
                m1.metric("Rows",    f"{before_r} → {after_r}",  delta=after_r-before_r)
                m2.metric("Columns", f"{before_c} → {after_c}",  delta=after_c-before_c)
                m3.metric("Missing", int(df_new.isnull().sum().sum()))

            except Exception as e:
                st.error(f"Operation failed: {e}")

    with right:
        st.markdown('<span class="sec-title">Missing Value Summary</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        miss_s = pd.DataFrame({
            "Missing": df_cur.isnull().sum(),
            "%": (df_cur.isnull().mean() * 100).round(2)
        }).sort_values("%", ascending=False)
        st.dataframe(miss_s.style.format({"%": "{:.2f}"}), use_container_width=True)

        missing_only = miss_s[miss_s["Missing"] > 0]
        if len(missing_only):
            import matplotlib.pyplot as plt
            _bg = "#1e1e2e" if IS_DARK else "#f9f8ff"
            _tc = "#f5f0ff" if IS_DARK else "#1a0030"
            fig, ax = plt.subplots(figsize=(7, max(2.2, len(missing_only) * 0.38)))
            fig.patch.set_facecolor(_bg); ax.set_facecolor(_bg)
            ax.barh(missing_only["Missing"].index[::-1], missing_only["%"][::-1],
                    color="#FF5EA3", edgecolor="none", height=0.55, alpha=0.88)
            ax.set_xlabel("Missing %", color=_tc, fontsize=8)
            ax.tick_params(colors=_tc, labelsize=7)
            for sp in ax.spines.values(): sp.set_edgecolor("none")
            ax.grid(axis="x", color="#3a2a4a" if IS_DARK else "#f0e0ea", linewidth=0.5)
            ax.set_title("Missing % by column", color=_tc, fontsize=9, fontweight="600")
            fig.tight_layout(pad=1.2)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DUPLICATES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    df = st.session_state["df"]
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Remove Duplicates</div></div>', unsafe_allow_html=True)

        dup_cols = st.multiselect("Subset columns (leave empty = all)", df.columns, key="dup_cols")
        keep     = st.selectbox("Keep", ["first", "last", "none"], key="dup_keep",
                                help="'none' removes ALL copies of a duplicated row")
        subset   = dup_cols if dup_cols else df.columns.tolist()

        if st.button("Remove Duplicates", key="dup_apply"):
            before = len(st.session_state["df"])
            keep_arg = False if keep == "none" else keep
            new_df = st.session_state["df"].drop_duplicates(subset=subset, keep=keep_arg)
            removed = before - len(new_df)
            st.session_state["df"] = new_df
            if removed == 0:
                st.info("No duplicates found — nothing removed.")
            else:
                log_action("Remove Duplicates", f"removed={removed}, keep={keep}, subset={subset}")
                st.success(f"✅ Removed {removed:,} duplicate rows")

    with right:
        st.markdown('<span class="sec-title">Duplicate Preview</span>', unsafe_allow_html=True)
        subset_preview = dup_cols if dup_cols else df.columns.tolist()
        dup_mask = df.duplicated(subset=subset_preview, keep=False)
        dup_df   = df[dup_mask]
        if len(dup_df) == 0:
            st.success("✅ No duplicates found in current dataset.")
        else:
            st.warning(f"{len(dup_df):,} rows involved in duplicates")
            st.dataframe(dup_df.head(200), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA TYPES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    df = st.session_state["df"]
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Cast Column Type</div></div>', unsafe_allow_html=True)

        dt_col    = st.selectbox("Column", df.columns, key="dt_col")
        dt_target = st.selectbox("Cast to", ["int", "float", "str", "datetime", "bool", "category"], key="dt_target")
        dt_fmt    = None
        if dt_target == "datetime":
            dt_fmt = st.text_input("Datetime format (optional, e.g. %Y-%m-%d)", key="dt_fmt")
        err_action = st.radio("On error", ["coerce (set NaN)", "raise"], horizontal=True, key="dt_err")

        if st.button("Cast Type", key="dt_apply"):
            df_new = st.session_state["df"].copy()
            errors_arg = "coerce" if "coerce" in err_action else "raise"
            try:
                if dt_target == "datetime":
                    df_new[dt_col] = pd.to_datetime(df_new[dt_col],
                                                    format=dt_fmt or None,
                                                    errors=errors_arg)
                elif dt_target == "int":
                    df_new[dt_col] = pd.to_numeric(df_new[dt_col], errors=errors_arg).astype("Int64")
                elif dt_target == "float":
                    df_new[dt_col] = pd.to_numeric(df_new[dt_col], errors=errors_arg)
                elif dt_target == "bool":
                    df_new[dt_col] = df_new[dt_col].astype(bool)
                elif dt_target == "category":
                    df_new[dt_col] = df_new[dt_col].astype("category")
                else:  # str
                    df_new[dt_col] = df_new[dt_col].astype(str)

                st.session_state["df"] = df_new
                log_action("Cast Type", f"{dt_col} → {dt_target}")
                st.success(f"✅ '{dt_col}' cast to {dt_target}")

            except Exception as e:
                st.error(f"Cast failed: {e}")

        st.markdown('<div class="op-hint">Use <strong>coerce</strong> to convert unparseable values to NaN instead of raising an error.</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<span class="sec-title">Column Types</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        type_df = pd.DataFrame({
            "Column":        df_cur.columns,
            "Current Type":  [str(df_cur[c].dtype) for c in df_cur.columns],
            "Non-Null":      df_cur.notnull().sum().values,
            "Unique":        df_cur.nunique().values,
        })
        st.dataframe(type_df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CATEGORICAL
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    df = st.session_state["df"]
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Encode &amp; Clean Categoricals</div></div>', unsafe_allow_html=True)

        if not cat_cols:
            st.info("No categorical columns detected in the current dataset.")
        else:
            cat_op = st.segmented_control("Operation", ["Label Encode", "One-Hot Encode", "Strip Whitespace", "To Lowercase", "Replace Value"], key="cat_op")

            cat_col_sel = st.multiselect("Columns", cat_cols, key="cat_col_sel")

            old_val = new_val = None
            if cat_op == "Replace Value" and cat_col_sel:
                old_val = st.text_input("Value to replace", key="cat_old")
                new_val = st.text_input("Replace with",     key="cat_new")

            if st.button("Apply", key="cat_apply"):
                if not cat_col_sel:
                    st.warning("Select at least one column.")
                else:
                    df_new = st.session_state["df"].copy()
                    try:
                        if cat_op == "Label Encode":
                            for c in cat_col_sel:
                                df_new[c] = df_new[c].astype("category").cat.codes
                            log_action("Label Encode", str(cat_col_sel))

                        elif cat_op == "One-Hot Encode":
                            df_new = pd.get_dummies(df_new, columns=cat_col_sel, drop_first=False)
                            log_action("One-Hot Encode", str(cat_col_sel))

                        elif cat_op == "Strip Whitespace":
                            for c in cat_col_sel:
                                df_new[c] = df_new[c].astype(str).str.strip()
                            log_action("Strip Whitespace", str(cat_col_sel))

                        elif cat_op == "To Lowercase":
                            for c in cat_col_sel:
                                df_new[c] = df_new[c].astype(str).str.lower()
                            log_action("To Lowercase", str(cat_col_sel))

                        elif cat_op == "Replace Value":
                            if old_val is None or old_val == "":
                                st.warning("Enter the value to replace.")
                            else:
                                for c in cat_col_sel:
                                    df_new[c] = df_new[c].replace(old_val, new_val)
                                log_action("Replace Value", f"{old_val} → {new_val} in {cat_col_sel}")

                        st.session_state["df"] = df_new
                        st.success("✅ Applied")

                    except Exception as e:
                        st.error(f"Operation failed: {e}")

    with right:
        st.markdown('<span class="sec-title">Value Counts Preview</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        cat_cur = df_cur.select_dtypes(include=["object", "category"]).columns.tolist()
        if cat_cur:
            preview_col = st.selectbox("Column to inspect", cat_cur, key="cat_preview")
            vc = df_cur[preview_col].value_counts(dropna=False).reset_index()
            vc.columns = ["Value", "Count"]
            vc["%"] = (vc["Count"] / len(df_cur) * 100).round(2)
            st.dataframe(vc, use_container_width=True)
        else:
            st.info("No categorical columns to preview.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — NUMERIC / OUTLIERS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    df = st.session_state["df"]
    num_cols = df.select_dtypes(include="number").columns.tolist()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Outlier Treatment</div></div>', unsafe_allow_html=True)

        if not num_cols:
            st.info("No numeric columns found.")
        else:
            out_col  = st.selectbox("Column", num_cols, key="out_col")
            out_meth = st.segmented_control("Detection", ["IQR", "Z-score"], key="out_meth")
            out_act  = st.segmented_control("Action", ["Remove Rows", "Cap (Winsorize)", "Replace with NaN"], key="out_act")

            z_thresh = 3.0
            if out_meth == "Z-score":
                z_thresh = st.number_input("Z-score threshold", 1.0, 10.0, 3.0, 0.5, key="out_z")

            iqr_mult = 1.5
            if out_meth == "IQR":
                iqr_mult = st.number_input("IQR multiplier", 0.5, 5.0, 1.5, 0.5, key="out_iqr")

            if st.button("Apply Outlier Treatment", key="out_apply"):
                df_new = st.session_state["df"].copy()
                col_data = df_new[out_col].dropna()

                try:
                    if out_meth == "IQR":
                        Q1, Q3 = col_data.quantile(0.25), col_data.quantile(0.75)
                        IQR = Q3 - Q1
                        lo, hi = Q1 - iqr_mult * IQR, Q3 + iqr_mult * IQR
                    else:  # Z-score
                        mu, sigma = col_data.mean(), col_data.std()
                        lo = mu - z_thresh * sigma
                        hi = mu + z_thresh * sigma

                    mask = (df_new[out_col] < lo) | (df_new[out_col] > hi)
                    n_out = int(mask.sum())

                    if out_act == "Remove Rows":
                        df_new = df_new[~mask]
                    elif out_act == "Cap (Winsorize)":
                        df_new[out_col] = df_new[out_col].clip(lower=lo, upper=hi)
                    else:  # Replace with NaN
                        df_new.loc[mask, out_col] = np.nan

                    st.session_state["df"] = df_new
                    log_action("Outlier Treatment", f"{out_col}, method={out_meth}, action={out_act}, n={n_out}")
                    st.success(f"✅ Treated {n_out:,} outlier(s) in '{out_col}'")

                except Exception as e:
                    st.error(f"Outlier treatment failed: {e}")

    with right:
        st.markdown('<span class="sec-title">Distribution Summary</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        num_cur = df_cur.select_dtypes(include="number").columns.tolist()
        if num_cur:
            dist_col = st.selectbox("Column to inspect", num_cur, key="out_dist_col")
            col_s = df_cur[dist_col].dropna()

            Q1, Q3 = col_s.quantile(0.25), col_s.quantile(0.75)
            IQR_   = Q3 - Q1
            lo_iqr = Q1 - 1.5 * IQR_
            hi_iqr = Q3 + 1.5 * IQR_
            n_out_iqr = int(((col_s < lo_iqr) | (col_s > hi_iqr)).sum())

            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Mean",   f"{col_s.mean():.2f}")
            d2.metric("Std",    f"{col_s.std():.2f}")
            d3.metric("Min",    f"{col_s.min():.2f}")
            d4.metric("Max",    f"{col_s.max():.2f}")

            st.caption(f"IQR outliers (×1.5): **{n_out_iqr}** rows below {lo_iqr:.2f} or above {hi_iqr:.2f}")

            import matplotlib.pyplot as plt
            _bg = "#1e1e2e" if IS_DARK else "#f9f8ff"
            _tc = "#f5f0ff" if IS_DARK else "#1a0030"
            fig, ax = plt.subplots(figsize=(7, 3))
            fig.patch.set_facecolor(_bg); ax.set_facecolor(_bg)
            ax.hist(col_s, bins=40, color="#FF5EA3", edgecolor="none", alpha=0.85)
            ax.axvline(lo_iqr, color="#a855f7", linewidth=1.2, linestyle="--", label="IQR lower")
            ax.axvline(hi_iqr, color="#a855f7", linewidth=1.2, linestyle="--", label="IQR upper")
            ax.set_xlabel(dist_col, color=_tc, fontsize=8)
            ax.tick_params(colors=_tc, labelsize=7)
            for sp in ax.spines.values(): sp.set_edgecolor("none")
            ax.legend(fontsize=7, facecolor=_bg, labelcolor=_tc)
            ax.set_title(f"Distribution: {dist_col}", color=_tc, fontsize=9, fontweight="600")
            fig.tight_layout(pad=1.2)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SCALING
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    df = st.session_state["df"]
    num_cols = df.select_dtypes(include="number").columns.tolist()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Scale Numeric Columns</div></div>', unsafe_allow_html=True)

        if not num_cols:
            st.info("No numeric columns found.")
        else:
            sc_cols   = st.multiselect("Columns to scale", num_cols, key="sc_cols")
            sc_method = st.segmented_control("Method", ["Min-Max (0–1)", "Z-score (Standardize)", "Robust"], key="sc_method")
            st.markdown(f"""<div class="op-hint">
              <strong>Min-Max</strong>: rescales to [0, 1].<br>
              <strong>Z-score</strong>: zero mean, unit variance.<br>
              <strong>Robust</strong>: uses median/IQR — better for outliers.
            </div>""", unsafe_allow_html=True)

            if st.button("Apply Scaling", key="sc_apply"):
                if not sc_cols:
                    st.warning("Select at least one column.")
                else:
                    df_new = st.session_state["df"].copy()
                    try:
                        valid = [c for c in sc_cols if df_new[c].notnull().sum() > 0]
                        if sc_method == "Min-Max (0–1)":
                            scaler = MinMaxScaler()
                            df_new[valid] = scaler.fit_transform(df_new[valid])
                        elif sc_method == "Z-score (Standardize)":
                            scaler = StandardScaler()
                            df_new[valid] = scaler.fit_transform(df_new[valid])
                        else:  # Robust
                            from sklearn.preprocessing import RobustScaler
                            scaler = RobustScaler()
                            df_new[valid] = scaler.fit_transform(df_new[valid])

                        st.session_state["df"] = df_new
                        log_action("Scaling", f"method={sc_method}, cols={valid}")
                        st.success(f"✅ Scaled {len(valid)} column(s)")
                    except Exception as e:
                        st.error(f"Scaling failed: {e}")

    with right:
        st.markdown('<span class="sec-title">Stats Before / After</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        num_cur = df_cur.select_dtypes(include="number").columns.tolist()
        if num_cur:
            st.dataframe(df_cur[num_cur].describe().T.round(4), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — COLUMNS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    df = st.session_state["df"]
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="op-panel"><div class="op-label">Operations</div><div class="op-title">Manage Columns</div></div>', unsafe_allow_html=True)

        col_op = st.segmented_control("Operation", ["Drop Columns", "Rename Column", "Reorder Columns"], key="col_op")

        if col_op == "Drop Columns":
            drop_sel = st.multiselect("Columns to drop", df.columns, key="col_drop")
            if st.button("Drop", key="col_drop_apply"):
                if not drop_sel:
                    st.warning("Select columns to drop.")
                else:
                    st.session_state["df"] = st.session_state["df"].drop(columns=drop_sel)
                    log_action("Drop Columns", str(drop_sel))
                    st.success(f"✅ Dropped: {drop_sel}")

        elif col_op == "Rename Column":
            ren_col = st.selectbox("Column to rename", df.columns, key="col_ren_src")
            ren_new = st.text_input("New name", key="col_ren_dst")
            if st.button("Rename", key="col_ren_apply"):
                if not ren_new.strip():
                    st.warning("Enter a new name.")
                elif ren_new in df.columns:
                    st.error("A column with that name already exists.")
                else:
                    st.session_state["df"] = st.session_state["df"].rename(columns={ren_col: ren_new})
                    log_action("Rename Column", f"{ren_col} → {ren_new}")
                    st.success(f"✅ Renamed '{ren_col}' → '{ren_new}'")

        elif col_op == "Reorder Columns":
            st.caption("Drag to reorder isn't available in Streamlit — use the list below to set order by selecting columns in your preferred sequence.")
            new_order = st.multiselect("Select columns in desired order", df.columns.tolist(),
                                       default=df.columns.tolist(), key="col_order")
            if st.button("Apply Order", key="col_order_apply"):
                missing_cols = [c for c in df.columns if c not in new_order]
                final_order  = new_order + missing_cols
                st.session_state["df"] = st.session_state["df"][final_order]
                log_action("Reorder Columns", str(final_order))
                st.success("✅ Columns reordered")

    with right:
        st.markdown('<span class="sec-title">Current Columns</span>', unsafe_allow_html=True)
        df_cur = st.session_state["df"]
        col_info = pd.DataFrame({
            "Column":  df_cur.columns,
            "Type":    [str(df_cur[c].dtype) for c in df_cur.columns],
            "Non-Null": df_cur.notnull().sum().values,
            "Unique":  df_cur.nunique().values,
        })
        st.dataframe(col_info, use_container_width=True, height=420)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    df_cur  = st.session_state["df"]
    df_orig = st.session_state.get("original_df", df_cur)

    st.markdown('<span class="sec-title">Dataset Comparison</span>', unsafe_allow_html=True)

    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Rows (original)",   f"{df_orig.shape[0]:,}")
    v2.metric("Rows (current)",    f"{df_cur.shape[0]:,}",  delta=df_cur.shape[0]-df_orig.shape[0])
    v3.metric("Cols (original)",   f"{df_orig.shape[1]}")
    v4.metric("Cols (current)",    f"{df_cur.shape[1]}",   delta=df_cur.shape[1]-df_orig.shape[1])

    st.markdown('<span class="sec-title">Missing Values Check</span>', unsafe_allow_html=True)
    total_miss = int(df_cur.isnull().sum().sum())
    if total_miss == 0:
        st.success("✅ No missing values remaining.")
    else:
        st.warning(f"⚠️ {total_miss:,} missing values remain.")
        miss_left = df_cur.isnull().sum()
        st.dataframe(miss_left[miss_left > 0].rename("Missing Count").reset_index().rename(columns={"index":"Column"}),
                     use_container_width=True)

    st.markdown('<span class="sec-title">Duplicate Check</span>', unsafe_allow_html=True)
    n_dupes = int(df_cur.duplicated().sum())
    if n_dupes == 0:
        st.success("✅ No duplicate rows remaining.")
    else:
        st.warning(f"⚠️ {n_dupes:,} duplicate rows remain.")

    st.markdown('<span class="sec-title">Data Types Overview</span>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({"Type": df_cur.dtypes.astype(str)}), use_container_width=True)

    st.markdown('<span class="sec-title">Transformation Log</span>', unsafe_allow_html=True)
    log = st.session_state.get("log", [])
    if log:
        for i, entry in enumerate(log, 1):
            st.markdown(f'<div class="log-entry"><strong>#{i}</strong> {entry["Action"]} — {entry["Detail"]}</div>', unsafe_allow_html=True)
    else:
        st.info("No transformations applied yet.")

    st.markdown("---")
    left_b, right_b = st.columns(2)
    with left_b:
        if st.button("⏪ Restore Original Dataset", key="val_restore"):
            if "original_df" in st.session_state:
                st.session_state["df"]  = st.session_state["original_df"].copy()
                st.session_state["log"] = []
                st.success("✅ Dataset restored to original.")
                st.rerun()
    with right_b:
        csv_out = df_cur.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Cleaned CSV", csv_out, "cleaned_data.csv", "text/csv", key="val_dl")
