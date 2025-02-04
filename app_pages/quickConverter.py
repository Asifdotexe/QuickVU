"""
This is the streamlit page for the QuickVU's universal file type convertor
"""

import pandas as pd
from io import BytesIO
import streamlit as st
from quickvu.universal_file_converter import (detect_file_type, read_file,
                                              get_conversion_options, convert_file)

with open('app_pages/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.markdown(
    '<h1 class="main-header">🔄 Quick Convert: File Format Converter</h1>',
    unsafe_allow_html=True)
st.markdown("""Quick Convert is a simple file format conversion tool. 
Upload your file, choose the desired output format, and download the converted file.""")

st.image('./artifacts/quick-converter-graphic.png', width=600)

# Sidebar - File upload
st.sidebar.image('./artifacts/logo-transparent.png', use_container_width=True)
st.sidebar.markdown('<h3 class="side-header">Upload Your File</h3>', unsafe_allow_html=True)


uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV, Excel, or JSON file",
    type=["csv", "xlsx", "xls", "json", "parquet"],
    help="Upload your artifacts in CSV, Excel, or JSON format for analysis.")

if uploaded_file:
    current_file_name, file_type = detect_file_type(uploaded_file.name)
    df = read_file(uploaded_file, file_type)

    if df is not None:
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        conversion_options = get_conversion_options(file_type)
        convert_to = st.sidebar.selectbox("Convert to format", conversion_options)

        if st.sidebar.button("Convert & Download"):
            output_path = convert_file(df, convert_to, current_file_name)

            if convert_to == "json":
                json_data = df.to_dict(
                    orient="records")  # Convert DataFrame to JSON format
                st.write("### JSON Preview")
                st.json(json_data[:5])  # Show only first 5 records for brevity

            elif convert_to == "xlsx" or "parquet":
                st.write("### Output Preview")
                st.dataframe(df.head())

    else:
        st.error("Unsupported file format. Please upload CSV, Excel, JSON, or Parquet.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Project by `Asif Sayyed`")
