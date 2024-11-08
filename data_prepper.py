import numpy as np
import pandas as pd
import streamlit as st
import quickvu.prepare_data as DataPrepper
from quickvu import eda 

st.markdown("""
    <style>
    body {
        background-color: #FFFFFF;
    }
    .main-header { 
        color: #0b78ee; 
        font-size: 34px; 
        font-weight: 700;
        text-align: left;
        margin-bottom: 20px;
    }
    .sub-header { 
        color: #0b78ee;
        font-size: 24px; 
        font-weight: 600; 
        margin: 20px 0;
    }
    .side-header {
        color: #0b78ee;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-divider {
        border-top: 2px solid #0b78ee;
        margin: 30px 0;
    }
    .instructions {
        font-size: 16px;
        color: #0b78ee;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Data Prepper: Data Cleaning Tool</h1>', unsafe_allow_html=True)
st.markdown("""
Data Prepper is a versatile data cleaning tool to help prepare your dataset for analysis.
Simply upload your data, select the desired cleaning options, and download the prepared data.
""")

# Sidebar - File upload
st.sidebar.image('./dataset/logo.png', use_column_width=True)
st.sidebar.markdown('<h3 class="side-header">Upload Dataset</h3>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Check if file is uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown('<h2 class="sub-header">Dataset Preview</h2>', unsafe_allow_html=True)
    st.write(df.head(10))

    # Cleaning options
    st.sidebar.markdown('<h3 class="side-header">Data Cleaning Options</h3>', unsafe_allow_html=True)
    
    show_summary_stats = st.sidebar.checkbox("Show Summary Statistics", help="Display summary statistics such as mean, median, and standard deviation for numerical columns.")
        
    # Standardize Column Names
    if st.sidebar.checkbox("Standardize Column Names", help="Convert column names to lowercase and replace spaces with underscores."):
        df = DataPrepper.standardize_column_names(df)

    # Handle Missing Values
    missing_value_option = st.sidebar.selectbox(
        "Handle Missing Values",
        ("None", "Fill with Mean", "Fill with Median", "Drop Missing Rows")
    )
    if missing_value_option == "Fill with Mean":
        df = DataPrepper.handle_missing_values(df, method='mean')
    elif missing_value_option == "Fill with Median":
        df = DataPrepper.handle_missing_values(df, method='median')
    elif missing_value_option == "Drop Missing Rows":
        df = DataPrepper.handle_missing_values(df)
                
    # Outlier Handling
    if st.sidebar.checkbox("Detect and Handle Outliers", help="Apply Z-score or IQR method to handle outliers."):
        outlier_method = st.sidebar.radio("Outlier Detection Method", ("Z-score", "IQR"))
        if outlier_method == "Z-score":
            df = DataPrepper.detech_outliers(df, method='zscore')
        elif outlier_method == "IQR":
            df = DataPrepper.detech_outliers(df, method='iqr')

    # Data Scaling
    if st.sidebar.checkbox("Scale Data", help="Standardize or normalize numerical columns."):
        scaling_method = st.sidebar.radio("Scaling Method", ("standarize", "normalize"))
        df = DataPrepper.scale_data(df, method=scaling_method)

    # Drop Duplicates
    if st.sidebar.checkbox("Drop Duplicate Rows", help="Remove duplicate rows in the dataset."):
        df = DataPrepper.remove_duplicates(df)

    # Column Manipulation
    if st.sidebar.checkbox("Add or Drop Columns", help="Add or drop specific columns."):
        column_action = st.sidebar.radio("Choose Action", ("Add Column", "Drop Column"))
        if column_action == "Add Column":
            new_column = st.sidebar.text_input("New Column Name", help="Enter the name for the new column.")
            default_value = st.sidebar.text_input("Default Value for New Column", help="Set a default value for this column.")
            if new_column:
                df[new_column] = default_value
        elif column_action == "Drop Column":
            column_to_drop = st.sidebar.selectbox("Select Column to Drop", df.columns.tolist())
            df = df.drop(columns=[column_to_drop])

    # Row Filtering
    if st.sidebar.checkbox("Filter Rows", help="Filter data by a column value or range."):
        filter_column = st.sidebar.selectbox("Select Column to Filter By", df.columns.tolist())
        unique_values = df[filter_column].unique()
        filter_values = st.sidebar.multiselect("Select Values to Keep", unique_values)
        if filter_values:
            df = df[df[filter_column].isin(filter_values)]

    # Display the cleaned dataset
    st.markdown('<h2 class="sub-header">Cleaned Dataset</h2>', unsafe_allow_html=True)
    st.write(df.head(10))
    
    if show_summary_stats:
        st.markdown('<h2 class="sub-header">Summary Statistics</h2>', unsafe_allow_html=True)
        st.write("Numerical:", eda.generate_summary_statistics(df))
        st.write("Categorical:", eda.generate_object_summary_statistics(df))

    # Download option
    st.sidebar.markdown('<h3 class="side-header">Download Cleaned Data</h3>', unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
else:
    st.markdown(
        '<p class="instructions">Please upload a CSV file to start data cleaning.</p>',
        unsafe_allow_html=True
    )

# Footer
st.sidebar.write("---")
st.sidebar.write("Data Prepper, part of the QuickVU ecosystem")
