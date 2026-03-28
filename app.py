import streamlit as st

st.set_page_config(layout="wide")

IS_DARK  = st.get_option("theme.base") == "dark"
TEXT_CLR = "#f5e6f0" if IS_DARK else "#1a0030"
SUB_CLR  = "#d4cce8" if IS_DARK else "#7a3058"
CARD_BG  = "rgba(40, 15, 35, 0.85)" if IS_DARK else "rgba(255,255,255,0.9)"

# ── CSS — no f-string interpolation inside card rule to avoid dark_mode error ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');

html, body, [class*="css"] {{ font-family: 'Quicksand', sans-serif !important; }}
.main .block-container {{
    padding-top: 2.5rem !important;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}}

/* ── Animated title ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(28px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}

.app-name {{
    font-family: 'Quicksand', sans-serif;
    font-size: 3.8rem; font-weight: 700; text-align: center;
    background: linear-gradient(90deg, #FF007F, #c084fc, #FF007F);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeUp .9s ease both, shimmer 3s linear infinite;
    animation-delay: 0s, .9s;
    letter-spacing: -1px; line-height: 1.15;
    margin-bottom: .3rem;
}}
.app-tagline {{
    text-align: center; font-size: 1.05rem;
    color: {SUB_CLR}; margin-bottom: 2.5rem;
    animation: fadeUp .9s ease .2s both;
}}
.app-divider {{
    width: 60px; height: 3px; margin: 0 auto 2.5rem;
    background: linear-gradient(90deg, #FF007F, #c084fc);
    border-radius: 4px;
    animation: fadeUp .9s ease .3s both;
}}

/* ── Feature cards ── */
.feat-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 16px; margin-bottom: 2.5rem;
    animation: fadeUp .9s ease .4s both;
}}
.feat-card {{
    border: 1.5px solid rgba(255,94,163,.28);
    border-radius: 16px; padding: 1.4rem 1.2rem;
    background: {CARD_BG}; text-align: center;
    transition: border-color .2s, transform .2s;
}}
.feat-card:hover {{ border-color: #FF007F; transform: translateY(-3px); }}
.feat-icon {{
    font-size: 1.8rem; margin-bottom: .6rem;
    display: block;
}}
.feat-title {{
    font-weight: 700; font-size: .95rem; color: {TEXT_CLR}; margin-bottom: .3rem;
}}
.feat-desc {{ font-size: .78rem; color: {SUB_CLR}; line-height: 1.5; }}

/* ── Lang pills ── */
.lang-row {{
    display: flex; justify-content: center; gap: 10px;
    margin-bottom: 2rem;
    animation: fadeUp .9s ease .5s both;
}}
.lang-pill {{
    border: 1.5px solid rgba(255,94,163,.35); border-radius: 20px;
    padding: 4px 16px; font-size: .78rem; font-weight: 600;
    color: {SUB_CLR}; cursor: pointer;
}}
.lang-pill.active {{
    background: linear-gradient(135deg,#FF007F,#c0006a);
    color: #fff; border-color: transparent;
}}

/* ── CTA ── */
.cta-wrap {{
    text-align: center; margin-bottom: 2rem;
    animation: fadeUp .9s ease .6s both;
}}
.cta-note {{ font-size: .82rem; color: {SUB_CLR}; margin-top: .6rem; }}

/* ── Buttons ── */
.stButton > button {{
    border: 1.5px solid #FF007F !important; color: #FF007F !important;
    background: transparent !important; border-radius: 8px !important;
    font-weight: 600 !important; font-family: 'Quicksand', sans-serif !important;
}}
.stButton > button:hover {{ background: rgba(255,0,127,.1) !important; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {{
    font-family: 'Quicksand', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# ── App name + tagline ────────────────────────────────────────────────────────
st.markdown('<div class="app-name">DataCraft</div>', unsafe_allow_html=True)
st.markdown('<div class="app-tagline">Clean · Transform · Visualize — all in one place.</div>', unsafe_allow_html=True)
st.markdown('<div class="app-divider"></div>', unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="feat-grid">
  <div class="feat-card">
    <span class="feat-icon">&#128194;</span>
    <div class="feat-title">Upload</div>
    <div class="feat-desc">CSV, Excel, JSON or Google Sheets</div>
  </div>
  <div class="feat-card">
    <span class="feat-icon">&#129529;</span>
    <div class="feat-title">Clean</div>
    <div class="feat-desc">Handle missing values, duplicates and outliers</div>
  </div>
  <div class="feat-card">
    <span class="feat-icon">&#128202;</span>
    <div class="feat-title">Visualize</div>
    <div class="feat-desc">9 chart types with filters and export</div>
  </div>
  <div class="feat-card">
    <span class="feat-icon">&#128229;</span>
    <div class="feat-title">Export</div>
    <div class="feat-desc">Download cleaned data, logs and reports</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-wrap">
  <div class="cta-note">Open the sidebar and go to Upload to get started.</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.info("Use the sidebar menu to navigate pages.")
