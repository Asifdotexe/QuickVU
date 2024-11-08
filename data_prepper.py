import numpy as np
import pandas as pd
import streamlit as st
import quickvu.prepare_data as DataPrepper
from quickvu import eda
from sklearn.preprocessing import StandardScaler, MinMaxScaler

st.markdown("""<style>... </style>""", unsafe_allow_html=True)  # Keep your styles here

# Header
st.markdown('<h1 class="main-header">Data Prepper: Data Cleaning Tool</h1>', unsafe_allow_html=True)
st.markdown("""Data Prepper is a versatile data cleaning tool to help prepare your dataset for analysis. Simply upload your data, select the desired cleaning options, and download the prepared data.""")

# Sidebar - File upload
st.sidebar.image('./dataset/logo.png', use_column_width=True)
st.sidebar.markdown('<h3 class="side-header">Upload Dataset</h3>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Check if file is uploaded
if uploaded_file:
    # Load the data into a DataFrame and store in session state
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)
    
    df = st.session_state.df  # Retrieve from session state
    
    st.markdown('<h2 class="sub-header">Dataset Preview</h2>', unsafe_allow_html=True)
    st.write(df.head(10))

    # Sidebar - Data Cleaning Options
    st.sidebar.markdown('<h3 class="side-header">Data Cleaning Options</h3>', unsafe_allow_html=True)

    # Show Summary Statistics
    show_summary_stats = st.sidebar.checkbox("Show Summary Statistics", help="Display summary statistics for numerical columns.")

    # Standardize Column Names
    if st.sidebar.checkbox("Standardize Column Names"):
        df = DataPrepper.standardize_column_names(df)
        st.session_state.df = df  # Save the modified df to session state

    # Handle Missing Values
    missing_value_option = st.sidebar.selectbox("Handle Missing Values", ("None", "Fill with Mean", "Fill with Median", "Drop Missing Rows"))
    if missing_value_option == "Fill with Mean":
        df = DataPrepper.handle_missing_values(df, method='mean')
    elif missing_value_option == "Fill with Median":
        df = DataPrepper.handle_missing_values(df, method='median')
    elif missing_value_option == "Drop Missing Rows":
        df = DataPrepper.handle_missing_values(df)
    st.session_state.df = df  # Save the modified df to session state

    # Outlier Handling with Column Selection
    if st.sidebar.checkbox("Detect and Handle Outliers"):
        outlier_columns = st.sidebar.multiselect("Select Columns for Outlier Treatment", df.select_dtypes(include=[np.number]).columns)
        outlier_method = st.sidebar.radio("Outlier Detection Method", ("Z-score", "IQR"))
        apply_outliers = st.sidebar.button("Apply Outlier Treatment")

        if apply_outliers and outlier_columns:
            if outlier_method == "Z-score":
                df = DataPrepper.detech_outliers(df, method='zscore', columns=outlier_columns)
            elif outlier_method == "IQR":
                df = DataPrepper.detech_outliers(df, method='iqr', columns=outlier_columns)
            st.write(f"Outliers detected and flagged in the selected columns: {', '.join(outlier_columns)}.")
            st.session_state.df = df  # Save the modified df to session state

    # Data Scaling with Column Selection
    if st.sidebar.checkbox("Scale Data"):
        scale_column = st.sidebar.selectbox("Select Column to Scale", df.select_dtypes(include=[np.number]).columns)
        scaling_method = st.sidebar.radio("Scaling Method", ("Standardize", "Normalize"))
        if st.sidebar.button("Apply Scaling"):
            if scaling_method == "Standardize":
                scaler = StandardScaler()
            else:
                scaler = MinMaxScaler()
            df[scale_column] = scaler.fit_transform(df[[scale_column]])
            st.session_state.df = df  # Save the modified df to session state

    # Drop Duplicate Rows
    if st.sidebar.checkbox("Drop Duplicate Rows"):
        df = DataPrepper.remove_duplicates(df)
        st.session_state.df = df  # Save the modified df to session state

    # Drop Columns
    if st.sidebar.checkbox("Drop Columns"):
        column_to_drop = st.sidebar.selectbox("Select Column to Drop", df.columns)
        if st.sidebar.button("Drop Column"):
            df = df.drop(columns=[column_to_drop])
            st.session_state.df = df  # Save the modified df to session state

    # Change Data Type
    if st.sidebar.checkbox("Change Data Type"):
        dtype_column = st.sidebar.selectbox("Select Column to Change Type", df.columns)
        dtype_option = st.sidebar.selectbox("Select Data Type", ["int", "float", "str","datetime"])
        if st.sidebar.button("Change Data Type"):
            df = DataPrepper.convert_data_types(df, {dtype_column: dtype_option})
            st.session_state.df = df  # Save the modified df to session state

    # Row Filtering
    if st.sidebar.checkbox("Filter Rows"):
        filter_column = st.sidebar.selectbox("Select Column to Filter By", df.columns)
        unique_values = df[filter_column].unique()
        filter_values = st.sidebar.multiselect("Select Values to Keep", unique_values)
        if filter_values:
            df = df[df[filter_column].isin(filter_values)]
            st.session_state.df = df  # Save the modified df to session state

    st.markdown('<h2 class="sub-header">Cleaned Dataset</h2>', unsafe_allow_html=True)
    st.write(df.head(10))

    st.markdown('<h2 class="sub-header">Summary Statistics</h2>', unsafe_allow_html=True)
    st.write("Numerical:", eda.generate_summary_statistics(df))
    st.write("Categorical:", eda.generate_object_summary_statistics(df))

    # Download option
    st.sidebar.markdown('<h3 class="side-header">Download Cleaned Data</h3>', unsafe_allow_html=True)
    csv = df.to_csv(index=False)
    st.sidebar.download_button("Download CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

else:
    st.markdown('<p class="instructions">Please upload a CSV file to start data cleaning.</p>', unsafe_allow_html=True)
