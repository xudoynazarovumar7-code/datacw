import streamlit as st

st.set_page_config(
    page_title="AI Data Wrangler",
    layout="wide"
)

st.title("AI-Assisted Data Wrangler & Visualizer")

st.write("""
This application allows users to:

• Upload datasets  
• Clean and transform data  
• Build visualizations  
• Export cleaned datasets
""")

st.info("Use the sidebar to navigate between pages.")