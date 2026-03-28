import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Upload & Overview", layout="wide")

@st.cache_data
def load_csv(file):   return pd.read_csv(file)
@st.cache_data
def load_excel(file): return pd.read_excel(file)

IS_DARK  = st.get_option("theme.base") == "dark"
TEXT_CLR = "#f5e6f0" if IS_DARK else "#1a0030"
SUB_CLR  = "#d4cce8" if IS_DARK else "#7a3058"
CARD_BG  = "rgba(40, 15, 35, 0.85)" if IS_DARK else "rgba(255,255,255,0.9)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');

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
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {{
    font-family: 'Quicksand', sans-serif !important;
}}

/* ── Fix overlay: push content below Streamlit toolbar ── */
.main .block-container {{
    padding-top: 2.5rem !important;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}}

/* ── Hero ── */
.upload-hero {{
    background: {"linear-gradient(120deg, #1a0030 0%, #3d0060 55%, #FF007F 100%)" if IS_DARK else "linear-gradient(120deg, #6b21a8 0%, #9333ea 55%, #FF007F 100%)"};
    border-radius: 16px; padding: 2rem 2.5rem 1.7rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}}
.upload-hero::before {{
    content: ""; position: absolute; right: -50px; top: -50px;
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,0,127,.28) 0%, transparent 70%);
}}
.upload-hero h1 {{
    font-weight: 700 !important; font-size: 2rem !important;
    color: #fff !important; margin: 0 0 .35rem !important;
}}
.upload-hero p {{
    color: rgba(255,255,255,.65) !important;
    margin: 0 !important; font-size: .92rem !important;
}}
.up-badge {{
    display: inline-block; background: rgba(255,255,255,.1);
    border: 1px solid rgba(255,255,255,.22); border-radius: 20px;
    padding: 2px 12px; font-size: .68rem; color: #ffb3d9;
    letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: .5rem;
}}

/* ── Step panels ── */
.step-panel {{
    border: 1.5px solid rgba(255,94,163,.3); border-radius: 14px;
    padding: 1.2rem 1.4rem; background: {CARD_BG};
    backdrop-filter: blur(6px); margin-bottom: .8rem;
}}
.step-label {{
    font-size: .68rem; font-weight: 700; letter-spacing: 1.4px;
    text-transform: uppercase; color: #FF5EA3; margin-bottom: .2rem;
}}
.step-title {{
    font-weight: 700; font-size: 1.2rem; color: {TEXT_CLR}; margin: 0;
}}
.step-hint {{
    font-size: .82rem; color: {SUB_CLR}; line-height: 1.65; margin-top: .6rem;
}}
.step-hint strong {{ color: #FF5EA3; }}

/* ── Metric cards ── */
.metric-row {{ display: flex; gap: 12px; margin: 1.6rem 0; flex-wrap: wrap; }}
.mc {{
    flex: 1; min-width: 110px; border-radius: 12px;
    padding: .85rem 1rem; text-align: center;
    border: 1.5px solid rgba(255,94,163,.3); background: {CARD_BG};
}}
.mc-val {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem; font-weight: 600; color: #FF5EA3;
}}
.mc-lbl {{
    font-size: .65rem; color: {SUB_CLR};
    text-transform: uppercase; letter-spacing: .9px; margin-top: 3px; font-weight: 700;
}}

/* ── Section title ── */
.sec-title {{
    font-weight: 700; font-size: 1.1rem; color: #FF5EA3;
    display: block; margin: 1.4rem 0 .8rem; padding-bottom: .3rem;
    border-bottom: 2px solid rgba(255,94,163,.3);
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

/* ── File uploader ── */
[data-testid="stFileUploader"] section {{
    border: 1.5px dashed rgba(255,0,127,.35) !important;
    border-radius: 10px !important;
}}

/* ── Expander spacing ── */
[data-testid="stExpander"] {{ margin-top: 1rem !important; }}
</style>
""", unsafe_allow_html=True)

# ── Session init ──────────────────────────────────────────────────────────────
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="upload-hero">
  <div class="up-badge">Page A · Upload &amp; Overview</div>
  <h1>Upload &amp; Data Overview</h1>
  <p>Load a CSV, Excel or JSON file — or connect a Google Sheet — to get started.</p>
</div>
""", unsafe_allow_html=True)

# ── Step 1 + 2 ────────────────────────────────────────────────────────────────
left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <div class="step-panel">
      <div class="step-label">Step 1</div>
      <div class="step-title">Select Data Source</div>
    </div>
    """, unsafe_allow_html=True)
    data_source = st.radio(
        "Choose how to load your data",
        ["Upload File", "Google Sheets"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown(f"""
    <div class="step-hint">
      Supported: <strong>CSV</strong>, <strong>Excel (.xlsx)</strong>, <strong>JSON</strong><br>
      Recommended minimum: 1,000 rows &middot; 8+ columns &middot; mixed types.
    </div>
    """, unsafe_allow_html=True)

df_loaded = None

with right:
    st.markdown("""
    <div class="step-panel">
      <div class="step-label">Step 2</div>
      <div class="step-title">Load Dataset</div>
    </div>
    """, unsafe_allow_html=True)

    if data_source == "Upload File":
        uploaded_file = st.file_uploader(
            "Drop your file here or click to browse",
            type=["csv", "xlsx", "json"],
            key=f"uploader_{st.session_state['uploader_key']}"
        )
        if uploaded_file:
            try:
                name = uploaded_file.name
                if name.endswith(".csv"):    df_loaded = load_csv(uploaded_file)
                elif name.endswith(".xlsx"): df_loaded = load_excel(uploaded_file)
                elif name.endswith(".json"): df_loaded = pd.read_json(uploaded_file)
                st.session_state["df"]          = df_loaded.copy()
                st.session_state["original_df"] = df_loaded.copy()
                if "log" not in st.session_state: st.session_state["log"] = []
                st.success(f"Loaded **{name}** — {df_loaded.shape[0]:,} rows, {df_loaded.shape[1]} columns")
            except Exception as e:
                st.error(f"Could not read file: {e}")
    else:
        url = st.text_input("Paste Google Sheets URL (must be publicly shared)")
        if url:
            try:
                sheet_id = url.split("/d/")[1].split("/")[0]
                csv_url  = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                df_loaded = pd.read_csv(csv_url)
                st.session_state["df"]          = df_loaded.copy()
                st.session_state["original_df"] = df_loaded.copy()
                if "log" not in st.session_state: st.session_state["log"] = []
                st.success(f"Google Sheet loaded — {df_loaded.shape[0]:,} rows, {df_loaded.shape[1]} columns")
            except Exception:
                st.error("Could not load sheet. Make sure it is set to 'Anyone with the link can view'.")

# ── Dataset overview ──────────────────────────────────────────────────────────
if "df" in st.session_state:
    df = st.session_state["df"]

    num_missing = int(df.isnull().sum().sum())
    num_dupes   = int(df.duplicated().sum())
    num_numeric = len(df.select_dtypes(include="number").columns)
    num_cat     = len(df.select_dtypes(include=["object", "category"]).columns)

    st.markdown(f"""
    <div class="metric-row">
      <div class="mc"><div class="mc-val">{df.shape[0]:,}</div><div class="mc-lbl">Rows</div></div>
      <div class="mc"><div class="mc-val">{df.shape[1]}</div><div class="mc-lbl">Columns</div></div>
      <div class="mc"><div class="mc-val">{num_numeric}</div><div class="mc-lbl">Numeric</div></div>
      <div class="mc"><div class="mc-val">{num_cat}</div><div class="mc-lbl">Categorical</div></div>
      <div class="mc"><div class="mc-val">{num_missing:,}</div><div class="mc-lbl">Missing</div></div>
      <div class="mc"><div class="mc-val">{num_dupes:,}</div><div class="mc-lbl">Duplicates</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sec-title">Explore Dataset</span>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Preview", "Column Types", "Missing Values", "Duplicates"])

    with tab1:
        n = st.slider("Rows to preview", 5, min(200, len(df)), 20, key="prev_n")
        st.dataframe(df.head(n), use_container_width=True)

    with tab2:
        dtypes_df = df.dtypes.reset_index()
        dtypes_df.columns = ["Column", "Type"]
        dtypes_df["Non-Null Count"] = df.notnull().sum().values
        dtypes_df["Unique Values"]  = df.nunique().values
        st.dataframe(dtypes_df, use_container_width=True)

    with tab3:
        miss = pd.DataFrame({
            "Column":        df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing %":     (df.isnull().mean() * 100).round(2).values
        }).sort_values("Missing Count", ascending=False)
        st.dataframe(miss, use_container_width=True)

        if num_missing > 0:
            miss_plot = miss[miss["Missing Count"] > 0]
            _bg = "#1e1e2e" if IS_DARK else "#fff8fb"
            _tc = "#f5f0ff" if IS_DARK else "#1a0030"
            fig, ax = plt.subplots(figsize=(9, max(2.5, len(miss_plot) * 0.42)))
            fig.patch.set_facecolor(_bg); ax.set_facecolor(_bg)
            ax.barh(miss_plot["Column"][::-1], miss_plot["Missing %"][::-1],
                    color="#FF5EA3", edgecolor="none", height=0.55, alpha=0.88)
            ax.set_xlabel("Missing %", color=_tc, fontsize=9)
            ax.tick_params(colors=_tc, labelsize=8)
            for sp in ax.spines.values(): sp.set_edgecolor("none")
            ax.grid(axis="x", color="#3a2a4a" if IS_DARK else "#f0e0ea", linewidth=0.6)
            ax.set_title("Missing values by column (%)", color=_tc, fontsize=10, fontweight="600")
            fig.tight_layout(pad=1.4)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with tab4:
        st.metric("Duplicate Rows", num_dupes)
        if num_dupes > 0:
            st.caption(f"{num_dupes} fully duplicated rows found. Use the Cleaning page to remove them.")
            if st.checkbox("Show duplicate rows"):
                st.dataframe(
                    df[df.duplicated(keep=False)].sort_values(df.columns[0]),
                    use_container_width=True
                )
        else:
            st.success("No duplicate rows detected.")

# ── Reset ─────────────────────────────────────────────────────────────────────
st.markdown("---")
if st.button("Reset Session"):
    st.session_state.clear()
    st.session_state["uploader_key"] = 1
    st.rerun()
