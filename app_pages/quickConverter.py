import streamlit as st
import pandas as pd

# Sidebar: Upload and select conversion options
st.sidebar.header("File Upload & Conversion")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "xls", "json", "parquet"])
convert_to = st.sidebar.selectbox("Convert to format", ["csv", "xlsx", "json", "parquet"])

if uploaded_file:
    # Detect file type
    file_type = uploaded_file.name.split(".")[-1]
    df = fc.read_file(uploaded_file, file_type)

    st.markdown("### Dataset Preview")
    st.write(df.head())

    # Convert and download button
    if st.sidebar.button("Convert and Download"):
        output_path = f"converted_file.{convert_to}"
        if convert_to == "csv":
            fc.convert_to_csv(df, output_path)
        elif convert_to == "xlsx":
            fc.convert_to_excel(df, output_path)
        elif convert_to == "json":
            fc.convert_to_json(df, output_path)
        elif convert_to == "parquet":
            fc.convert_to_parquet(df, output_path)

        st.success(f"File converted to {convert_to.upper()} format! Download below:")
        st.download_button("Download Converted File", data=open(output_path, "rb"), file_name=output_path)
