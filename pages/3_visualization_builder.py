import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
import io, warnings
warnings.filterwarnings("ignore")

# ── Theme ─────────────────────────────────────────────────────────────────────
IS_DARK   = st.get_option("theme.base") == "dark"
FIG_BG    = "#1e0a18" if IS_DARK else "#fff8fb"
GRID_CLR  = "#3a1a2e" if IS_DARK else "#f5e0ec"
SPINE_CLR = "#5a2040" if IS_DARK else "#e8c0d5"
TEXT_CLR  = "#f5e6f0" if IS_DARK else "#1a0030"
SUB_CLR   = "#d4cce8" if IS_DARK else "#7a3058"
LEGEND_FC = "#2e0d20" if IS_DARK else "#fff0f7"
CARD_BG  = "rgba(40, 15, 35, 0.85)" if IS_DARK else "rgba(255,255,255,0.9)"
BORD_CLR  = "rgba(255,94,163,0.3)"

PALETTE = ["#FF5EA3","#f472b6","#fb7185","#e879f9","#c084fc","#60a5fa","#34d399"]
ACCENT  = "#FF5EA3"
YELLOW  = "#fbbf24"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

html, body {{ font-family: 'Quicksand', sans-serif !important; }}
.stMarkdown, .stMarkdown p, .stMarkdown span,
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
[data-testid="stExpander"] summary p {{
    font-family: 'Quicksand', sans-serif !important;
}}
[data-testid="stExpander"] {{
    margin-top: 1rem !important;
}}
.main .block-container {{
    padding-top: 2.5rem !important;
    max-width: 1100px;
    position: relative;
    z-index: 1;
}}

/* ── Hero ── */
.viz-hero {{
    background: {"linear-gradient(120deg, #1a0030 0%, #3d0060 55%, #FF007F 100%)" if IS_DARK else "linear-gradient(120deg, #6b21a8 0%, #9333ea 55%, #FF007F 100%)"};
    border-radius: 16px; padding: 2rem 2.5rem 1.7rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}}
.viz-hero::before {{
    content: ""; position: absolute; right: -50px; top: -50px;
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,0,127,.28) 0%, transparent 70%);
}}
.viz-hero h1 {{
    font-weight: 700 !important; font-size: 2rem !important;
    color: #fff !important; margin: 0 0 .35rem !important;
}}
.viz-hero p {{ color: rgba(255,255,255,.6) !important; margin: 0 !important; font-size: .92rem !important; }}
.viz-badge {{
    display: inline-block; background: rgba(255,255,255,.1);
    border: 1px solid rgba(255,255,255,.22); border-radius: 20px;
    padding: 2px 12px; font-size: .68rem; color: #ffb3d9;
    letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: .5rem;
}}

/* ── Metric cards ── */
.metric-row {{ display: flex; gap: 12px; margin-bottom: 1.6rem; flex-wrap: wrap; }}
.mc {{
    flex: 1; min-width: 100px; border-radius: 12px;
    padding: .85rem 1rem; text-align: center;
    border: 1.5px solid {BORD_CLR}; background: {CARD_BG};
}}
.mc-val {{ font-family: 'JetBrains Mono', monospace !important; font-size: 1.5rem; font-weight: 600; color: #FF5EA3; }}
.mc-lbl {{ font-size: .65rem; color: {SUB_CLR}; text-transform: uppercase; letter-spacing: .9px; margin-top: 3px; font-weight: 700; }}

/* ── Section title ── */
.sec-title {{
    font-weight: 700 !important; font-size: 1.1rem !important;
    color: #FF5EA3 !important;
    margin: 1.4rem 0 .8rem; padding-bottom: .3rem;
    border-bottom: 2px solid rgba(255,94,163,.3);
    display: block;
}}

/* ── Suggestion cards ── */
.sug-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-top: .8rem; }}
.sug-card {{
    border: 1.5px solid {BORD_CLR}; border-radius: 12px;
    padding: 1rem 1.1rem; height: 88px;
    display: flex; flex-direction: column; justify-content: center;
    background: {CARD_BG};
}}
.sug-card strong {{ color: #FF5EA3; font-size: .87rem; }}
.sug-card p {{ font-size: .75rem; color: {SUB_CLR}; margin: 4px 0 0; line-height: 1.35; }}

/* ── Buttons ── */
.stDownloadButton > button {{
    background: linear-gradient(135deg, #FF007F, #c0006a) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
}}
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

/* ── Select/input labels ── */
.stSelectbox label, .stMultiSelect label, .stSlider label, .stNumberInput label {{
    font-size: .75rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: .7px !important;
    color: {SUB_CLR} !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.markdown('<div class="viz-hero"><div class="viz-badge">Page C</div>'
                '<h1>Chart Studio</h1><p>Upload a dataset first.</p></div>', unsafe_allow_html=True)
    st.stop()

df = st.session_state["df"].copy()
for col in df.columns:
    try: df[col] = pd.to_numeric(df[col])
    except: pass

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include=["object","category"]).columns.tolist()
dt_cols  = df.select_dtypes(include="datetime64").columns.tolist()
all_cols = df.columns.tolist()

# ── Hero + Metrics ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="viz-hero">
  <div class="viz-badge">Page C · Visualization Builder</div>
  <h1>Chart Studio</h1>
  <p>Build charts from your cleaned dataset — filter, aggregate, and export.</p>
</div>
<div class="metric-row">
  <div class="mc"><div class="mc-val">{len(df):,}</div><div class="mc-lbl">Rows</div></div>
  <div class="mc"><div class="mc-val">{len(all_cols)}</div><div class="mc-lbl">Columns</div></div>
  <div class="mc"><div class="mc-val">{len(num_cols)}</div><div class="mc-lbl">Numeric</div></div>
  <div class="mc"><div class="mc-val">{len(cat_cols)}</div><div class="mc-lbl">Categorical</div></div>
  <div class="mc"><div class="mc-val">{len(dt_cols)}</div><div class="mc-lbl">Datetime</div></div>
</div>
""", unsafe_allow_html=True)

# ── Chart helpers ─────────────────────────────────────────────────────────────
def make_fig(w=9, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(FIG_BG); ax.set_facecolor(FIG_BG)
    ax.tick_params(labelsize=9, colors=TEXT_CLR)
    for sp in ax.spines.values(): sp.set_edgecolor(SPINE_CLR)
    ax.xaxis.label.set_color(TEXT_CLR); ax.yaxis.label.set_color(TEXT_CLR)
    ax.title.set_color(TEXT_CLR)
    ax.grid(True, color=GRID_CLR, linewidth=0.6)
    fig.tight_layout(pad=1.8)
    return fig, ax

def style_ax(ax):
    ax.set_facecolor(FIG_BG); ax.tick_params(labelsize=8, colors=TEXT_CLR)
    for sp in ax.spines.values(): sp.set_edgecolor(SPINE_CLR)
    ax.xaxis.label.set_color(TEXT_CLR); ax.yaxis.label.set_color(TEXT_CLR)
    ax.title.set_color(TEXT_CLR)
    ax.grid(True, color=GRID_CLR, linewidth=0.5)

def style_legend(legend):
    legend.get_frame().set_facecolor(LEGEND_FC); legend.get_frame().set_edgecolor(SPINE_CLR)
    for t in legend.get_texts(): t.set_color(TEXT_CLR)
    if legend.get_title(): legend.get_title().set_color(TEXT_CLR)

def to_png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    return buf.getvalue()

CHART_TYPES = ["Histogram","Box Plot","Scatter","Line Chart","Bar Chart",
               "Heatmap","Violin","Area Chart","3D Scatter"]

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_auto, tab_custom, tab_dash = st.tabs(["Auto Insights", "Custom Builder", "Dashboard"])

# ══ TAB 1: Auto Insights ══════════════════════════════════════════════════════
with tab_auto:
    if not num_cols and not cat_cols:
        st.warning("No plottable columns detected."); st.stop()

    if num_cols:
        st.markdown('<span class="sec-title">Numeric Distributions</span>', unsafe_allow_html=True)
        for c in num_cols[:4]:
            fig, ax = make_fig(9, 3.5); data = df[c].dropna()
            ax.hist(data, bins=28, color=ACCENT, edgecolor=FIG_BG, linewidth=.4, alpha=.88)
            ax.axvline(data.mean(),   color=YELLOW, lw=1.8, linestyle="--", label=f"Mean {data.mean():.2f}")
            ax.axvline(data.median(), color="#fb7185", lw=1.8, linestyle=":",  label=f"Median {data.median():.2f}")
            ax.set_title(f"Distribution — {c}", fontweight="700", fontsize=11)
            ax.set_xlabel(c); style_legend(ax.legend(fontsize=8))
            st.pyplot(fig, use_container_width=True)
            st.download_button(f"Download — {c}", to_png(fig), f"dist_{c}.png", key=f"dai_{c}")
            plt.close(fig)

    if cat_cols:
        st.markdown('<span class="sec-title">Top Categories</span>', unsafe_allow_html=True)
        for c in cat_cols[:3]:
            vc = df[c].value_counts().head(10); fig, ax = make_fig(9, 3.5)
            ax.barh(vc.index[::-1], vc.values[::-1],
                    color=[PALETTE[i%len(PALETTE)] for i in range(len(vc))][::-1],
                    edgecolor="none", height=.6)
            for b in ax.patches:
                ax.text(b.get_width() + max(vc.values)*0.01, b.get_y()+b.get_height()/2,
                        f"{int(b.get_width()):,}", va="center", fontsize=8, color=TEXT_CLR)
            ax.set_title(f"Top values — {c}", fontweight="700", fontsize=11)
            ax.tick_params(colors=TEXT_CLR)
            st.pyplot(fig, use_container_width=True)
            st.download_button(f"Download — {c}", to_png(fig), f"top_{c}.png", key=f"dac_{c}")
            plt.close(fig)

    if len(num_cols) >= 2:
        st.markdown('<span class="sec-title">Correlation Matrix</span>', unsafe_allow_html=True)
        corr = df[num_cols].corr(); n = len(num_cols)
        fig, ax = plt.subplots(figsize=(max(6,n*.7+1), max(4,n*.7)))
        fig.patch.set_facecolor(FIG_BG); ax.set_facecolor(FIG_BG)
        sns.heatmap(corr, ax=ax, annot=True, fmt=".2f",
                    cmap=sns.diverging_palette(330, 10, l=50, s=90, as_cmap=True),
                    linewidths=1, linecolor=FIG_BG,
                    annot_kws={"size":8,"color":TEXT_CLR}, cbar_kws={"shrink":.8})
        ax.tick_params(colors=TEXT_CLR, labelsize=9)
        ax.set_xticklabels(ax.get_xticklabels(), color=TEXT_CLR)
        ax.set_yticklabels(ax.get_yticklabels(), color=TEXT_CLR)
        ax.set_title("Pearson Correlation", color=TEXT_CLR, fontsize=12, fontweight="700")
        ax.collections[0].colorbar.ax.tick_params(colors=TEXT_CLR)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        st.download_button("Download Heatmap", to_png(fig), "correlation.png", key="dai_corr")
        plt.close(fig)

        st.markdown('<span class="sec-title">Scatter Overview</span>', unsafe_allow_html=True)
        ca, cb = num_cols[0], num_cols[1]; fig, ax = make_fig(9, 4.5)
        if cat_cols:
            for i, cat in enumerate(df[cat_cols[0]].dropna().unique()[:7]):
                m = df[cat_cols[0]] == cat
                ax.scatter(df.loc[m,ca], df.loc[m,cb], label=str(cat),
                           color=PALETTE[i%len(PALETTE)], alpha=.65, s=22, edgecolors="none")
            style_legend(ax.legend(title=cat_cols[0], fontsize=8))
        else:
            ax.scatter(df[ca], df[cb], color=ACCENT, alpha=.55, s=18, edgecolors="none")
        valid = df[[ca,cb]].dropna()
        if len(valid) > 5:
            try:
                z = np.polyfit(valid[ca], valid[cb], 1)
                xs = np.linspace(valid[ca].min(), valid[ca].max(), 200)
                ax.plot(xs, np.poly1d(z)(xs), "--", color=YELLOW, lw=1.5, alpha=.85)
            except: pass
        ax.set_xlabel(ca); ax.set_ylabel(cb)
        ax.set_title(f"{ca} vs {cb}", fontweight="700", fontsize=11)
        st.pyplot(fig, use_container_width=True)
        st.download_button("Download Scatter", to_png(fig), "scatter_auto.png", key="dai_sc")
        plt.close(fig)

# ══ TAB 2: Custom Builder ═════════════════════════════════════════════════════
with tab_custom:
    st.markdown('<span class="sec-title">Build a Chart</span>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns([1.2,1,1,1])
    with c1: chart_type = st.selectbox("Chart type", CHART_TYPES, key="ct")
    with c2:
        if chart_type == "Heatmap":
            x_col = st.multiselect("Columns", num_cols, default=num_cols[:min(5,len(num_cols))], key="hm"); y_col=None
        elif chart_type in ["Histogram","Box Plot","Violin"]:
            x_col = st.selectbox("Column", num_cols or all_cols, key="cx"); y_col=None
        elif chart_type == "3D Scatter":
            x_col = st.selectbox("X axis", num_cols, key="cx3"); y_col=None
        else:
            x_col = st.selectbox("X axis", all_cols, key="cx2")
            y_col = st.selectbox("Y axis", num_cols or all_cols, key="cy2")
    with c3:
        z_col=color_col=agg_func=top_n=None
        if chart_type == "3D Scatter":
            y_col = st.selectbox("Y axis", num_cols, key="cy3")
            z_col = st.selectbox("Z axis", num_cols, key="cz3")
        elif chart_type != "Heatmap" and cat_cols:
            color_col = st.selectbox("Group / color", ["None"]+cat_cols, key="cc")
            if color_col == "None": color_col = None
    with c4:
        if chart_type in ["Bar Chart","Line Chart","Area Chart"]:
            agg_func = st.selectbox("Aggregation", ["mean","sum","count","median"], key="cagg")
        if chart_type == "Bar Chart":
            top_n = st.number_input("Top N", 3, 50, 10, key="ctopn")

    with st.expander("Filter data before plotting"):
        fdf = df.copy(); fa,fb = st.columns(2)
        with fa:
            if cat_cols:
                fc = st.selectbox("Category filter", ["None"]+cat_cols, key="fcat")
                if fc != "None":
                    opts = df[fc].dropna().unique().tolist()
                    sel  = st.multiselect(f"Keep '{fc}'", opts, default=opts, key="fcat_v")
                    fdf  = fdf[fdf[fc].isin(sel)]
        with fb:
            if num_cols:
                fn = st.selectbox("Numeric range", ["None"]+num_cols, key="fnum")
                if fn != "None":
                    mn,mx = float(df[fn].min()), float(df[fn].max())
                    rng = st.slider(f"Range '{fn}'", mn, mx, (mn,mx), key="fnum_r")
                    fdf = fdf[(fdf[fn]>=rng[0])&(fdf[fn]<=rng[1])]
        st.caption(f"Rows in view: **{len(fdf):,}** / {len(df):,}")

    if st.button("Generate Chart", key="gen"):
        try:
            fig = ax = None; ct = chart_type
            if ct == "Heatmap":
                cols_sel = x_col if isinstance(x_col,list) and len(x_col)>=2 else num_cols[:6]
                corr = fdf[cols_sel].corr(); sz = max(5,len(cols_sel)*.8)
                fig,ax = plt.subplots(figsize=(sz+1,sz))
                fig.patch.set_facecolor(FIG_BG); ax.set_facecolor(FIG_BG)
                sns.heatmap(corr, ax=ax, annot=True, fmt=".2f",
                            cmap=sns.diverging_palette(330,10,l=50,s=90,as_cmap=True),
                            linewidths=1, linecolor=FIG_BG, annot_kws={"size":8,"color":TEXT_CLR})
                ax.tick_params(colors=TEXT_CLR)
                ax.set_xticklabels(ax.get_xticklabels(), color=TEXT_CLR)
                ax.set_yticklabels(ax.get_yticklabels(), color=TEXT_CLR)
                ax.set_title("Correlation Heatmap", color=TEXT_CLR, fontweight="700"); fig.tight_layout()
                ax.collections[0].colorbar.ax.tick_params(colors=TEXT_CLR)
            elif ct == "3D Scatter":
                if x_col and y_col and z_col:
                    fig = plt.figure(figsize=(8,6)); fig.patch.set_facecolor(FIG_BG)
                    ax = fig.add_subplot(111, projection="3d"); ax.set_facecolor(FIG_BG)
                    ax.scatter(fdf[x_col], fdf[y_col], fdf[z_col], c=ACCENT, alpha=.65, s=18)
                    ax.set_xlabel(x_col, color=TEXT_CLR); ax.set_ylabel(y_col, color=TEXT_CLR)
                    ax.set_zlabel(z_col, color=TEXT_CLR); ax.tick_params(colors=TEXT_CLR)
                    ax.set_title("3D Scatter", color=TEXT_CLR, fontweight="700"); fig.tight_layout()
            elif ct == "Histogram":
                fig,ax = make_fig(); data = fdf[x_col].dropna()
                ax.hist(data, bins=30, color=ACCENT, edgecolor=FIG_BG, linewidth=.4, alpha=.9)
                ax.axvline(data.mean(),   color=YELLOW,    lw=1.8, linestyle="--", label=f"Mean {data.mean():.2f}")
                ax.axvline(data.median(), color="#fb7185", lw=1.8, linestyle=":",  label=f"Median {data.median():.2f}")
                ax.set_title(f"Distribution — {x_col}", fontweight="700"); ax.set_xlabel(x_col)
                style_legend(ax.legend(fontsize=8))
            elif ct == "Box Plot":
                fig,ax = make_fig()
                if color_col:
                    groups=[fdf[fdf[color_col]==v][x_col].dropna() for v in fdf[color_col].unique()[:8]]
                    labels=[str(v) for v in fdf[color_col].unique()[:8]]
                    bp=ax.boxplot(groups,patch_artist=True,medianprops=dict(color=YELLOW,lw=2))
                    for p,c in zip(bp["boxes"],PALETTE): p.set_facecolor(c); p.set_alpha(.75)
                    ax.set_xticklabels(labels,rotation=30,ha="right",color=TEXT_CLR)
                else:
                    bp=ax.boxplot(fdf[x_col].dropna(),patch_artist=True,medianprops=dict(color=YELLOW,lw=2))
                    bp["boxes"][0].set_facecolor(ACCENT); bp["boxes"][0].set_alpha(.75)
                ax.set_title(f"Box Plot — {x_col}", fontweight="700")
            elif ct == "Violin":
                fig,ax = make_fig()
                groups=[fdf[fdf[color_col]==v][x_col].dropna().values for v in fdf[color_col].unique()[:8]] if color_col else [fdf[x_col].dropna().values]
                groups=[g for g in groups if len(g)>1]
                if groups:
                    vp=ax.violinplot(groups,showmedians=True)
                    for i,b in enumerate(vp["bodies"]): b.set_facecolor(PALETTE[i%len(PALETTE)]); b.set_alpha(.75)
                    vp["cmedians"].set_color(YELLOW)
                ax.set_title(f"Violin — {x_col}", fontweight="700"); ax.set_ylabel(x_col)
            elif ct == "Scatter":
                fig,ax = make_fig(9,5.5)
                if color_col:
                    for i,cat in enumerate(fdf[color_col].dropna().unique()[:8]):
                        m=fdf[color_col]==cat
                        ax.scatter(fdf.loc[m,x_col],fdf.loc[m,y_col],label=str(cat),
                                   color=PALETTE[i%len(PALETTE)],alpha=.65,s=24,edgecolors="none")
                    style_legend(ax.legend(title=color_col,fontsize=8))
                else:
                    ax.scatter(fdf[x_col],fdf[y_col],color=ACCENT,alpha=.55,s=20,edgecolors="none")
                valid=fdf[[x_col,y_col]].dropna()
                if pd.api.types.is_numeric_dtype(valid[x_col]) and len(valid)>5:
                    try:
                        z=np.polyfit(valid[x_col],valid[y_col],1)
                        xs=np.linspace(valid[x_col].min(),valid[x_col].max(),200)
                        ax.plot(xs,np.poly1d(z)(xs),"--",color=YELLOW,lw=1.5,alpha=.85)
                    except: pass
                ax.set_xlabel(x_col); ax.set_ylabel(y_col)
                ax.set_title(f"{x_col} vs {y_col}", fontweight="700")
            elif ct == "Line Chart":
                func=agg_func or "mean"; grp=fdf.groupby(x_col)[y_col].agg(func)
                fig,ax=make_fig(9,4.5)
                ax.plot(range(len(grp)),grp.values,color=ACCENT,lw=2.5,marker="o",markersize=3)
                ax.fill_between(range(len(grp)),grp.values,alpha=.15,color=ACCENT)
                ax.set_xticks(range(len(grp))); ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=8,color=TEXT_CLR)
                ax.set_xlabel(x_col); ax.set_ylabel(f"{func}({y_col})")
                ax.set_title(f"Line — {func}({y_col}) by {x_col}", fontweight="700")
            elif ct == "Bar Chart":
                func=agg_func or "mean"
                if color_col:
                    grp=fdf.groupby([x_col,color_col])[y_col].agg(func).unstack(color_col)
                    if top_n: grp=grp.loc[grp.sum(axis=1).nlargest(int(top_n)).index]
                    fig,ax=make_fig(10,5); w=0.8/max(len(grp.columns),1); xp=np.arange(len(grp))
                    for i,col in enumerate(grp.columns[:8]):
                        ax.bar(xp+i*w,grp[col],width=w,label=str(col),color=PALETTE[i%len(PALETTE)],edgecolor="none",alpha=.9)
                    ax.set_xticks(xp+w*(len(grp.columns)-1)/2)
                    ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=8,color=TEXT_CLR)
                    style_legend(ax.legend(title=color_col,fontsize=8))
                else:
                    grp=fdf.groupby(x_col)[y_col].agg(func)
                    if top_n: grp=grp.nlargest(int(top_n))
                    fig,ax=make_fig(10,5)
                    bars=ax.bar(range(len(grp)),grp.values,
                                color=[PALETTE[i%len(PALETTE)] for i in range(len(grp))],edgecolor="none",alpha=.9)
                    ax.set_xticks(range(len(grp)))
                    ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=8,color=TEXT_CLR)
                    for b in bars:
                        ax.text(b.get_x()+b.get_width()/2,b.get_height()*1.015,
                                f"{b.get_height():,.1f}",ha="center",va="bottom",fontsize=7.5,color=TEXT_CLR)
                ax.set_xlabel(x_col); ax.set_ylabel(f"{func}({y_col})")
                ax.set_title(f"Bar — {func}({y_col}) by {x_col}", fontweight="700")
            elif ct == "Area Chart":
                func=agg_func or "mean"; grp=fdf.groupby(x_col)[y_col].agg(func)
                fig,ax=make_fig(9,4.5)
                ax.fill_between(range(len(grp)),grp.values,alpha=.3,color=ACCENT)
                ax.plot(range(len(grp)),grp.values,color=ACCENT,lw=2.5)
                ax.set_xticks(range(len(grp)))
                ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=8,color=TEXT_CLR)
                ax.set_xlabel(x_col); ax.set_ylabel(f"{func}({y_col})")
                ax.set_title(f"Area — {func}({y_col}) by {x_col}", fontweight="700")
            if fig:
                st.pyplot(fig, use_container_width=True)
                st.download_button("Download Chart", to_png(fig), "chart.png", key="dl_cust")
                plt.close(fig)
        except Exception as e:
            st.error(f"Chart error: {e}")
            st.caption("Verify that selected columns contain compatible data for this chart type.")

    st.markdown("---")
    st.markdown('<span class="sec-title">Chart Suggestions</span>', unsafe_allow_html=True)
    if st.button("Suggest charts for my data", key="suggest"):
        sugs=[]
        if len(num_cols)>=2:
            sugs.append(("Scatter Plot", f"Explore the relationship between {num_cols[0]} and {num_cols[1]}"))
            sugs.append(("Correlation Heatmap", "All numeric correlations at a glance"))
        if cat_cols and num_cols:
            sugs.append(("Grouped Bar Chart", f"Compare {num_cols[0]} across {cat_cols[0]}"))
            sugs.append(("Violin Plot", f"Distribution of {num_cols[0]} grouped by {cat_cols[0]}"))
        if num_cols: sugs.append(("Histogram", f"Distribution shape of {num_cols[0]}"))
        if dt_cols and num_cols: sugs.append(("Line Chart", f"Trend of {num_cols[0]} over time"))
        if sugs:
            cards = "".join(f'<div class="sug-card"><strong>{t}</strong><p>{d}</p></div>' for t,d in sugs)
            st.markdown(f'<div class="sug-grid">{cards}</div>', unsafe_allow_html=True)
        else:
            st.info("Load a dataset with numeric and categorical columns to see suggestions.")

# ══ TAB 3: Dashboard ══════════════════════════════════════════════════════════
with tab_dash:
    st.markdown('<span class="sec-title">2x2 Dashboard Builder</span>', unsafe_allow_html=True)
    st.caption("Configure four panels independently, then render as a single exportable dashboard.")
    cfgs=[]
    for i in range(4):
        with st.expander(f"Panel {i+1}", expanded=(i==0)):
            pa,pb,pc = st.columns(3)
            with pa: ct=st.selectbox("Type",["Histogram","Bar Chart","Scatter","Box Plot","Line Chart"],key=f"dt_{i}")
            with pb:
                if ct in ["Histogram","Box Plot"]: xc=st.selectbox("Column",num_cols or all_cols,key=f"dx_{i}"); yc=None
                else: xc=st.selectbox("X",all_cols,key=f"dx_{i}"); yc=st.selectbox("Y",num_cols or all_cols,key=f"dy_{i}")
            with pc:
                ag=st.selectbox("Aggregation",["mean","sum","count"],key=f"da_{i}") if ct=="Bar Chart" else "mean"
            cfgs.append({"type":ct,"x":xc,"y":yc,"agg":ag})

    if st.button("Render Dashboard", key="dash"):
        try:
            fig=plt.figure(figsize=(14,9)); fig.patch.set_facecolor(FIG_BG)
            gs=gridspec.GridSpec(2,2,figure=fig,hspace=.45,wspace=.32)
            for idx,cfg in enumerate(cfgs):
                ax=fig.add_subplot(gs[idx//2,idx%2]); style_ax(ax)
                try:
                    ct,xc,yc,ag=cfg["type"],cfg["x"],cfg["y"],cfg["agg"]; color=PALETTE[idx%len(PALETTE)]
                    if ct=="Histogram":
                        d=df[xc].dropna(); ax.hist(d,bins=20,color=color,edgecolor=FIG_BG,alpha=.88)
                        ax.axvline(d.mean(),color=YELLOW,lw=1.3,linestyle="--")
                        ax.set_title(f"Dist: {xc}",fontsize=9,fontweight="700",color=TEXT_CLR)
                    elif ct=="Box Plot":
                        bp=ax.boxplot(df[xc].dropna(),patch_artist=True,medianprops=dict(color=YELLOW,lw=2))
                        bp["boxes"][0].set_facecolor(color); bp["boxes"][0].set_alpha(.75)
                        ax.set_title(f"Box: {xc}",fontsize=9,fontweight="700",color=TEXT_CLR)
                    elif ct=="Scatter" and yc:
                        ax.scatter(df[xc],df[yc],color=color,alpha=.5,s=12,edgecolors="none")
                        ax.set_xlabel(xc,fontsize=7.5,color=TEXT_CLR); ax.set_ylabel(yc,fontsize=7.5,color=TEXT_CLR)
                        ax.set_title(f"{xc} vs {yc}",fontsize=9,fontweight="700",color=TEXT_CLR)
                    elif ct=="Bar Chart" and yc:
                        grp=df.groupby(xc)[yc].agg(ag).nlargest(8)
                        ax.bar(range(len(grp)),grp.values,color=[PALETTE[j%len(PALETTE)] for j in range(len(grp))],edgecolor="none",alpha=.9)
                        ax.set_xticks(range(len(grp))); ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=7,color=TEXT_CLR)
                        ax.set_title(f"{ag}({yc}) by {xc}",fontsize=9,fontweight="700",color=TEXT_CLR)
                    elif ct=="Line Chart" and yc:
                        grp=df.groupby(xc)[yc].agg(ag)
                        ax.plot(range(len(grp)),grp.values,color=color,lw=2)
                        ax.fill_between(range(len(grp)),grp.values,alpha=.15,color=color)
                        ax.set_xticks(range(len(grp))); ax.set_xticklabels(grp.index,rotation=35,ha="right",fontsize=7,color=TEXT_CLR)
                        ax.set_title(f"{ag}({yc})",fontsize=9,fontweight="700",color=TEXT_CLR)
                    ax.tick_params(colors=TEXT_CLR,labelsize=7.5)
                except Exception as ce:
                    ax.text(.5,.5,f"Error:\n{ce}",ha="center",va="center",transform=ax.transAxes,color="#fb7185",fontsize=8)
            fig.suptitle("Data Dashboard",color=TEXT_CLR,fontsize=14,fontweight="bold",y=1.01)
            st.pyplot(fig,use_container_width=True)
            st.download_button("Download Dashboard",to_png(fig),"dashboard.png",key="dl_dash")
            plt.close(fig)
        except Exception as e:
            st.error(f"Dashboard error: {e}")
