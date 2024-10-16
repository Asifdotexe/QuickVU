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
    st.sidebar.header("Select Columns for Analysis")
    
    # Dynamically get column names and their types
    columns = df.columns.tolist()
    column_types = df.dtypes

    # Let user select any column for analysis
    selected_columns = st.sidebar.multiselect("Select Columns", columns)

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

    if st.sidebar.checkbox("Show Correlation Matrix"):
        st.write("## Correlation Matrix")
        fig = eda.plot_correlation_matrix(df_clean)
        st.pyplot(fig)

    # Check selected columns for analysis
    numerical_columns = df_clean.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()

    if st.sidebar.checkbox("Plot Sales Trends"):
        st.write("## Sales Trends Over Time")
        if len(selected_columns) >= 2:  # Check if at least two columns are selected
            date_col = st.sidebar.selectbox("Select Purchase Date Column", [col for col in selected_columns if column_types[col] == 'datetime64[ns]'])
            amount_col = st.sidebar.selectbox("Select Sales Amount Column", [col for col in selected_columns if column_types[col] in ['float64', 'int64']])
            fig = eda.plot_sales_trends(df_clean, date_col, amount_col)
            st.pyplot(fig)
        else:
            st.warning("Please select at least two columns for this analysis.")

    # Step 6: Visualization
    st.sidebar.header("Data Visualization")
    
    if st.sidebar.checkbox("Plot Sales by Product"):
        st.write("## Sales by Product")
        if 'product' in selected_columns and 'sales' in selected_columns:  # Use relevant names for checks
            product_col = st.sidebar.selectbox("Select Product Column", [col for col in selected_columns if col in categorical_columns])
            sales_col = st.sidebar.selectbox("Select Sales Amount Column", [col for col in selected_columns if column_types[col] in ['float64', 'int64']])
            fig = visualization.plot_sales_by_product(df_clean, product_col, sales_col)
            st.pyplot(fig)
        else:
            st.warning("Please select both Product and Sales Amount columns for this analysis.")

    if st.sidebar.checkbox("Customer Demographics"):
        st.write("## Customer Demographics")
        if 'customer' in selected_columns and 'sales' in selected_columns:  # Use relevant names for checks
            customer_col = st.sidebar.selectbox("Select Customer ID Column", [col for col in selected_columns if col in categorical_columns])
            sales_col = st.sidebar.selectbox("Select Sales Amount Column", [col for col in selected_columns if column_types[col] in ['float64', 'int64']])
            fig = visualization.plot_customer_demographics(df_clean, customer_col, sales_col)
            st.pyplot(fig)
        else:
            st.warning("Please select both Customer ID and Sales Amount columns for this analysis.")

    # Step 7: Predictive Modeling (Optional)
    st.sidebar.header("Predictive Modeling (Optional)")
    if st.sidebar.checkbox("Build Sales Forecast Model"):
        st.write("## Sales Forecast Model")
        feature_column = st.sidebar.selectbox("Select Feature (Optional)", selected_columns)
        target_column = st.sidebar.selectbox("Select Target Column (Sales Amount)", [col for col in selected_columns if column_types[col] in ['float64', 'int64']])

        if feature_column and target_column:
            model, metrics = modeling.build_sales_forecast_model(df_clean, [feature_column], target_column)
            st.write(f"Mean Squared Error (MSE): {metrics['mse']}")
        else:
            st.warning("Please select both Feature and Target columns for the model.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Powered by `customer_analysis_tool`")
