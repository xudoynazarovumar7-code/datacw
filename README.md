# DataCraft — Data Cleaning and Visualization Platform

## Overview

DataCraft is an interactive web-based application developed using Streamlit that supports the full data analysis workflow. The system enables users to upload datasets, perform data cleaning and transformation, generate visualizations, and export structured analytical reports.

The primary goal of the application is to provide a unified and user-friendly environment for exploratory data analysis and preprocessing, with an emphasis on transparency, reproducibility, and practical usability.

---

## Objectives

* To simplify the data preprocessing and cleaning process
* To provide interactive tools for exploratory data analysis
* To enable efficient visualization of structured datasets
* To maintain a clear record of all transformation steps
* To support exportable outputs suitable for reporting and documentation

---

## Functional Components

### 1. Data Upload and Overview

The application supports multiple data sources:

* CSV files
* Excel files (.xlsx)
* JSON files
* Google Sheets (via public link)

Upon loading a dataset, the system provides an overview including:

* Number of rows and columns
* Missing values summary
* Duplicate record detection

---

### 2. Data Cleaning and Transformation

The cleaning module provides a comprehensive set of preprocessing tools.

**Missing Value Handling**

* Removal of rows or columns with missing data
* Imputation using:

  * Mean, median, or mode
  * Constant values
  * Forward fill and backward fill

**Duplicate Management**

* Detection and removal of duplicate records
* Custom subset selection for duplicate checks

**Data Type Conversion**

* Conversion between numeric, categorical, datetime, and boolean formats
* Error handling options for invalid conversions

**Feature Processing**

* Encoding of categorical variables
* Outlier handling using statistical techniques
* Feature scaling:

  * Min-Max normalization
  * Standardization

**Transformation Logging**

* All operations are recorded
* Enables reproducibility and auditability of the workflow

---

### 3. Visualization Module

The application provides both automated insights and custom visualization capabilities.

**Automated Insights**

* Distribution plots for numeric variables
* Frequency analysis for categorical variables
* Correlation matrix visualization
* Scatter plots with trend estimation

**Custom Visualization Builder**
Supported chart types include:

* Histogram
* Box plot
* Scatter plot
* Line chart
* Bar chart
* Heatmap
* Violin plot
* Area chart
* 3D scatter plot

Additional features:

* Data filtering prior to visualization
* Aggregation functions (mean, sum, count, median)
* Export of charts as image files

---

### 4. Export and Reporting

The system provides multiple export options:

* Cleaned dataset export
* Transformation log download
* Automatically generated reports:

  * Text-based analytical report
  * Multi-sheet Excel report
  * JSON representation of transformation steps

---

## Project Structure

```
DataCraft
│
├── app.py
├── pages/
│   ├── 1_upload_overview.py
│   ├── 2_cleaning_studio.py
│   ├── 3_visualization_builder.py
│   └── 4_export_report.py
│
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/datacraft.git
cd datacraft
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

4. Open the application in a browser:

```
http://localhost:8501
```

---

## Deployment

The application can be deployed using Streamlit Cloud.

Steps:

1. Upload the project to a GitHub repository
2. Create a new app on Streamlit Cloud
3. Select the repository and main file (`app.py`)
4. Ensure that all dependencies are listed in `requirements.txt`
5. (Optional) Specify Python version using `runtime.txt`

---

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SciPy
* Scikit-learn
* OpenPyXL

---

## Use Cases

* Academic data analysis projects
* Exploratory data analysis (EDA)
* Data preprocessing demonstrations
* Rapid development of analytical dashboards
* Report generation for structured datasets

---

## Limitations

* Performance may decrease with very large datasets
* Certain operations require properly formatted input data
* Some statistical methods are limited to numeric data types


---

## License

This project is intended for academic and educational use.
