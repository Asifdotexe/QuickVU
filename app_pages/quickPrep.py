import numpy as np
import pandas as pd
import streamlit as st
import quickvu.prepare_data as DataPrepper
from quickvu import eda
from sklearn.preprocessing import StandardScaler, MinMaxScaler

with open('app_pages/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧹 Quick Prep: Data Cleaning Tool</h1>', unsafe_allow_html=True)

st.image('./dataset/quickPrepDiagram.png')

st.markdown("""Quick Prep is a versatile data cleaning tool to help prepare your dataset for analysis. Simply upload your data, select the desired cleaning options, and download the prepared data.""")

# Sidebar - File upload
st.sidebar.image('./dataset/logo-png.png', use_container_width=True)

st.sidebar.markdown('<h3 class="side-header">Upload your Dataset</h3>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a CSV, Excel, or JSON file", type=["csv", "xlsx", "xls", "json"], help="Upload your dataset in CSV, Excel, or JSON format for analysis.")

if uploaded_file:
    try:
        # Read data based on file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        
        # Display preview of the dataset
        st.markdown('<h2 class="sub-header">Dataset Preview</h2>', unsafe_allow_html=True)
        st.write(df.head(10))
    
    except Exception as e:
        st.error(f"Error loading file: {e}")

    # Sidebar - Data Cleaning Options
    st.sidebar.markdown('<h3 class="side-header">Data Cleaning Options</h3>', unsafe_allow_html=True)

    # Show Summary Statistics
    show_summary_stats = st.sidebar.checkbox("Show Summary Statistics", help="Display summary statistics for numerical columns.")

    # Standardize Column Names
    if st.sidebar.checkbox("Standardize Column Names", help="Standardizes column names to lower case and replaces spaces with underscores."):
        df = DataPrepper.standardize_column_names(df)
        st.session_state.df = df

    # Handle Missing Values
    missing_value_option = st.sidebar.selectbox("Handle Missing Values", 
                                                ("None", "Fill with Mean", "Fill with Median", "Drop Missing Rows"),
                                                help="Choose how to handle missing values in the dataset.")
    if missing_value_option == "Fill with Mean":
        df = DataPrepper.handle_missing_values(df, method='mean')
        st.session_state.df = df
    elif missing_value_option == "Fill with Median":
        df = DataPrepper.handle_missing_values(df, method='median')
        st.session_state.df = df
    elif missing_value_option == "Drop Missing Rows":
        df = DataPrepper.handle_missing_values(df)
        st.session_state.df = df

    # Outlier Handling with Column Selection
    if st.sidebar.checkbox("Detect and Handle Outliers", help="Select columns and choose a method to detect and handle outliers in the dataset."):
        outlier_columns = st.sidebar.multiselect("Select Columns for Outlier Treatment", df.select_dtypes(include=[np.number]).columns)
        outlier_method = st.sidebar.radio("Outlier Detection Method", ("Z-score", "IQR"))
        apply_outliers = st.sidebar.button("Apply Outlier Treatment", help="Marks outliers as TRUE, non-outliers as FALSE.")

        if apply_outliers and outlier_columns:
            if outlier_method == "Z-score":
                df = DataPrepper.detech_outliers(df, method='zscore', columns=outlier_columns)
                st.session_state.df = df
            elif outlier_method == "IQR":
                df = DataPrepper.detech_outliers(df, method='iqr', columns=outlier_columns)
                st.session_state.df = df 

    # Data Scaling with Column Selection
    if st.sidebar.checkbox("Scale Data", help="Select a column to scale and choose the scaling method (Standardize or Normalize)."):
        scale_column = st.sidebar.selectbox("Select Column to Scale", df.select_dtypes(include=[np.number]).columns)
        scaling_method = st.sidebar.radio("Scaling Method", ("Standardize", "Normalize"))
        if st.sidebar.button("Apply Scaling"):
            if scaling_method == "Standardize":
                scaler = StandardScaler()
            else:
                scaler = MinMaxScaler()
            df[scale_column] = scaler.fit_transform(df[[scale_column]])
            st.session_state.df = df 

    # Drop Duplicate Rows
    if st.sidebar.checkbox("Drop Duplicate Rows", help="Drop duplicate rows from the dataset."):
        df = DataPrepper.remove_duplicates(df)
        st.session_state.df = df 
    # Drop Columns
    if st.sidebar.checkbox("Drop Columns", help="Select and remove a column from the dataset."):
        column_to_drop = st.sidebar.selectbox("Select Column to Drop", df.columns)
        if st.sidebar.button("Drop Column"):
            df = df.drop(columns=[column_to_drop])
            st.session_state.df = df

    # Change Data Type
    if st.sidebar.checkbox("Change Data Type", help="Change the data type of a selected column."):
        dtype_column = st.sidebar.selectbox("Select Column to Change Type", df.columns)
        dtype_option = st.sidebar.selectbox("Select Data Type", ["int", "float", "str", "datetime"])
        if st.sidebar.button("Change Data Type"):
            df = DataPrepper.convert_data_types(df, {dtype_column: dtype_option})
            st.session_state.df = df 

    # Row Filtering
    if st.sidebar.checkbox("Filter Rows", help="Filter rows based on selected values from a specific column."):
        filter_column = st.sidebar.selectbox("Select Column to Filter By", df.columns)
        unique_values = df[filter_column].unique()
        filter_values = st.sidebar.multiselect("Select Values to Keep", unique_values)
        if filter_values:
            df = df[df[filter_column].isin(filter_values)]
            st.session_state.df = df 

    # Display Cleaned Dataset
    st.markdown('<h2 class="sub-header">Cleaned Dataset</h2>', unsafe_allow_html=True)
    st.write(df.head(10))

    st.markdown('<h2 class="sub-header">Summary Statistics</h2>', unsafe_allow_html=True)
    st.write("Numerical:", eda.generate_summary_statistics(df))
    st.write("Categorical:", eda.generate_object_summary_statistics(df))

    # Download option
    st.sidebar.markdown('<h3 class="side-header">Download Cleaned Data</h3>', unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.sidebar.download_button("Download CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv", help="Download the cleaned data as a CSV file.")

else:
    st.markdown('<p class="instructions">Please upload a file to start data cleaning. </br> You can drop the file at the data uploader located on the navigation side bar. </p>', unsafe_allow_html=True)

# Footer
st.sidebar.write("---")
st.sidebar.write("Project by `Asif Sayyed`")