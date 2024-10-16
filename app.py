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
    
    # Step 3: Preprocessing
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
    
    # Step 4: Exploratory Data Analysis
    st.sidebar.header("Exploratory Data Analysis")
    if st.sidebar.checkbox("Show Summary Statistics"):
        st.write("## Summary Statistics")
        st.write(eda.generate_summary_statistics(df_clean))
    
    if st.sidebar.checkbox("Plot Sales Trends"):
        st.write("## Sales Trends Over Time")
        fig = eda.plot_sales_trends(df_clean, Config.PURCHASE_DATE, Config.SALES_AMOUNT)
        st.pyplot(fig)
    
    if st.sidebar.checkbox("Show Correlation Matrix"):
        st.write("## Correlation Matrix")
        fig = eda.plot_correlation_matrix(df_clean)
        st.pyplot(fig)

    # Step 5: Visualization
    st.sidebar.header("Data Visualization")
    if st.sidebar.checkbox("Plot Sales by Product"):
        st.write("## Sales by Product")
        fig = visualization.plot_sales_by_product(df_clean, Config.PRODUCT_ID, Config.SALES_AMOUNT)
        st.pyplot(fig)
    
    if st.sidebar.checkbox("Customer Demographics"):
        st.write("## Customer Demographics")
        fig = visualization.plot_customer_demographics(df_clean, Config.CUSTOMER_ID, Config.SALES_AMOUNT)
        st.pyplot(fig)

    # Step 6: Predictive Modeling (Optional)
    st.sidebar.header("Predictive Modeling (Optional)")
    if st.sidebar.checkbox("Build Sales Forecast Model"):
        st.write("## Sales Forecast Model")
        feature_column = st.sidebar.selectbox("Select Feature", df_clean.columns)
        target_column = Config.SALES_AMOUNT

        model, metrics = modeling.build_sales_forecast_model(df_clean, [feature_column], target_column)
        st.write(f"Mean Squared Error (MSE): {metrics['mse']}")

# Footer
st.sidebar.write("---")
st.sidebar.write("Powered by `customer_analysis_tool`")
