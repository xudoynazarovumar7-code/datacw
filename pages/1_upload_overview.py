import streamlit as st
import pandas as pd

st.title("Upload & Data Overview")

st.subheader("Choose Data Source")

data_source = st.radio(
    "Select data source:",
    ["Upload File", "Google Sheets"]
)

df = None


# -------------------------------
# OPTION 1: FILE UPLOAD
# -------------------------------

if data_source == "Upload File":

    uploaded_file = st.file_uploader(
        "Upload dataset",
        type=["csv", "xlsx", "json"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        elif uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)


# -------------------------------
# OPTION 2: GOOGLE SHEETS
# -------------------------------

if data_source == "Google Sheets":

    sheet_url = st.text_input(
        "Paste Google Sheets link"
    )

    if sheet_url:

        try:

            # convert google sheet url → csv export
            sheet_id = sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

            df = pd.read_csv(csv_url)

            st.success("Google Sheet loaded successfully")

        except:
            st.error("Invalid Google Sheets link")


# -------------------------------
# DATA OVERVIEW
# -------------------------------

if df is not None:

    st.session_state["df"] = df

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Shape")

    rows, cols = df.shape

    col1, col2 = st.columns(2)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)

    st.subheader("Column Data Types")
    st.write(df.dtypes)

    st.subheader("Missing Values")

    missing = df.isnull().sum()
    st.write(missing)

    st.subheader("Duplicate Rows")

    duplicates = df.duplicated().sum()
    st.write(f"Duplicate rows: {duplicates}")


# -------------------------------
# RESET SESSION
# -------------------------------

if st.button("Reset Session"):

    st.session_state.clear()

    st.success("Session reset")