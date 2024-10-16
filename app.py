import streamlit as st
import pandas as pd
from customer_analysis_tool import data_processing, eda, visualization, modeling
from customer_analysis_tool.config import Config
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("Customer Sales and Marketing Data Analysis Tool")

# Step 1: Data Upload
st.sidebar.header("Upload your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    # Step 2: Load the dataset
    df = pd.read_csv(uploaded_file)
    st.write("## Dataset Preview")
    st.write(df.head())
    
    # Step 3: Column Selection
    st.sidebar.header("Select Columns (Optional)")
    customer_id = st.sidebar.selectbox('Select Customer ID Column (Optional)', [''] + list(df.columns))
    sales_amount = st.sidebar.selectbox('Select Sales Amount Column (Optional)', [''] + list(df.columns))
    purchase_date = st.sidebar.selectbox('Select Purchase Date Column (Optional)', [''] + list(df.columns))
    product_id = st.sidebar.selectbox('Select Product ID Column (Optional)', [''] + list(df.columns))
    marketing_spend = st.sidebar.selectbox('Select Marketing Spend Column (Optional)', [''] + list(df.columns))

    # Step 4: Preprocessing Options
    st.sidebar.header("Preprocessing Options")
    missing_value_option = st.sidebar.selectbox(
        "How do you want to handle missing values?",
        ("Fill with Mean", "Fill with Median", "Drop Missing Rows")
    )
    
    if missing_value_option == "Fill with Mean":
        Config.FILL_MISSING_METHOD = 'mean'
    elif missing_value_option == "Fill with Median":
        Config.FILL_MISSING_METHOD = 'median'
    else:
        Config.FILL_MISSING_METHOD = 'drop'
    
    # Apply preprocessing
    st.write("## Preprocessed Dataset")
    df_clean = data_processing.preprocess_data(df)
    st.write(df_clean.head())
    
    # Step 5: Exploratory Data Analysis
    st.sidebar.header("Exploratory Data Analysis")
    if st.sidebar.checkbox("Show Summary Statistics"):
        st.write("## Summary Statistics")
        st.write(eda.generate_summary_statistics(df_clean))
    
    if st.sidebar.checkbox("Plot Sales Trends"):
        st.write("## Sales Trends Over Time")
        if purchase_date and sales_amount:
            fig = eda.plot_sales_trends(df_clean, purchase_date, sales_amount)
            st.pyplot(fig)
        else:
            st.warning("Please select both Purchase Date and Sales Amount columns for this analysis.")
    
    if st.sidebar.checkbox("Show Correlation Matrix"):
        st.write("## Correlation Matrix")
        fig = eda.plot_correlation_matrix(df_clean)
        st.pyplot(fig)

    # Step 6: Visualization
    st.sidebar.header("Data Visualization")
    if st.sidebar.checkbox("Plot Sales by Product"):
        st.write("## Sales by Product")
        if product_id and sales_amount:
            fig = visualization.plot_sales_by_product(df_clean, product_id, sales_amount)
            st.pyplot(fig)
        else:
            st.warning("Please select both Product ID and Sales Amount columns for this analysis.")
    
    if st.sidebar.checkbox("Customer Demographics"):
        st.write("## Customer Demographics")
        if customer_id and sales_amount:
            fig = visualization.plot_customer_demographics(df_clean, customer_id, sales_amount)
            st.pyplot(fig)
        else:
            st.warning("Please select both Customer ID and Sales Amount columns for this analysis.")

    # Step 7: Predictive Modeling (Optional)
    st.sidebar.header("Predictive Modeling (Optional)")
    if st.sidebar.checkbox("Build Sales Forecast Model"):
        st.write("## Sales Forecast Model")
        feature_column = st.sidebar.selectbox("Select Feature (Optional)", df_clean.columns)
        target_column = sales_amount if sales_amount else st.sidebar.selectbox("Select Target Column (Sales Amount)", df_clean.columns)

        if feature_column and target_column:
            model, metrics = modeling.build_sales_forecast_model(df_clean, [feature_column], target_column)
            st.write(f"Mean Squared Error (MSE): {metrics['mse']}")
        else:
            st.warning("Please select both Feature and Target columns for the model.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Powered by `customer_analysis_tool`")
