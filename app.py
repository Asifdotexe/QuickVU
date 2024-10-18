import streamlit as st
import numpy as np
import pandas as pd
from customer_analysis_tool import data_processing, eda, visualization, modeling
from customer_analysis_tool.config import Config
import matplotlib.pyplot as plt
import seaborn as sns
import datahorse

# Function to convert integer columns to datetime if they represent dates
def convert_int_to_datetime(df):
    for col in df.columns:
        if df[col].dtype == 'int64':
            # Check if the integer represents a date in 'YYYYMMDD' format
            if df[col].between(19000101, 21001231).all():  # Adjust this range based on your data
                df[col] = pd.to_datetime(df[col], format='%Y%m%d', errors='coerce')
            # Check if the integer represents a Unix timestamp
            elif df[col].between(0, 2147483647).all():  # Typical range for Unix timestamps
                df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')
    return df

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
    
    # Step 3: Convert integer columns to datetime
    df = convert_int_to_datetime(df)
    
    # Step 4: Dynamically get column names and their types
    columns = df.columns.tolist()
    column_types = df.dtypes

    # Separate columns by type
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_columns = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

    # Let user select columns for analysis
    st.sidebar.header("Select Columns for Analysis")
    selected_categorical = st.sidebar.multiselect("Select Categorical Columns", categorical_columns)
    selected_numerical = st.sidebar.multiselect("Select Numerical Columns", numerical_columns)
    selected_datetime = st.sidebar.multiselect("Select Date/Time Columns", datetime_columns)

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
        # Check if any numerical columns are selected
        if selected_numerical:
            # Filter the DataFrame to include only selected numerical columns
            df_numerical = df_clean[selected_numerical]
            # Calculate the correlation matrix
            correlation_matrix = df_numerical.corr()
            # Plot the correlation matrix
            fig = plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
            plt.title('Correlation Matrix of Selected Numerical Columns')
            st.pyplot(fig)
        else:
            st.warning("Please select at least one Numerical column to show the correlation matrix.")

    # Plot Sales Trends only if there are datetime columns
    if selected_datetime:  # Ensure that there are datetime columns selected
        if st.sidebar.checkbox("Plot Sales Trends"):
            st.write("## Sales Trends Over Time")
            if selected_numerical:  # Ensure at least one numerical column is selected
                date_col = st.sidebar.selectbox("Select Purchase Date Column (Optional)", selected_datetime, key="date_col")
                amount_col = st.sidebar.selectbox("Select Sales Amount Column", selected_numerical, key="amount_col")
                if date_col is not None:  # Check if a datetime column is selected
                    fig = eda.plot_sales_trends(df_clean, date_col, amount_col)
                    st.pyplot(fig)
                else:
                    st.warning("No Date/Time column selected. Sales trends will not be plotted.")
            else:
                st.warning("Please select at least one Numerical column for this analysis.")
    else:
        st.warning("No Date/Time columns available for trend analysis.")

    # Step 6: Visualization
    st.sidebar.header("Data Visualization")
    
    if st.sidebar.checkbox("Plot Sales by Product"):
        st.write("## Sales by Product")
        if selected_categorical and selected_numerical:  # Ensure at least one column from each type is selected
            product_col = st.sidebar.selectbox("Select Product Column", selected_categorical, key="product_col")
            sales_col = st.sidebar.selectbox("Select Sales Amount Column", selected_numerical, key="sales_col")
            fig = visualization.plot_sales_by_product(df_clean, product_col, sales_col)
            st.pyplot(fig)
        else:
            st.warning("Please select both a Categorical and a Numerical column for this analysis.")

    # DataHorse Interaction for specific tasks
    # st.sidebar.write("---")
    # st.sidebar.write("DataHorse Interaction")
    # chart_prompt = st.sidebar.checkbox("Prompt to Chart")
    
    # if chart_prompt:
    #     description_prompt = st.text_input("Describe the data analysis you'd like to perform (e.g., summarize data, convert categorical to numeric, etc.)")
        
    #     if st.button("Analyze with DataHorse"):
    #         try:
    #             df_dh = datahorse.read(uploaded_file)  # Wrap the DataFrame for DataHorse interaction
                
    #             # Prompt DataHorse to analyze
    #             response = df_dh.chat(description_prompt, seed=int, cache_req=True)
    #             st.write("### DataHorse Response")
    #             st.pyplot(response)

    #         except Exception as e:
    #             st.error(f"An error occurred: {e}")
                
# Step 7: Predictive Modeling (Optional)
# st.sidebar.header("Predictive Modeling (Optional)")
# if st.sidebar.checkbox("Build Sales Forecast Model"):
#     st.write("## Sales Forecast Model")
#     feature_column = st.sidebar.selectbox("Select Feature (Optional)", selected_numerical, key="feature_col")
#     target_column = st.sidebar.selectbox("Select Target Column (Sales Amount)", selected_numerical, key="target_col")

#     if feature_column and target_column:
#         # Build the sales forecast model
#         model, metrics = modeling.build_sales_forecast_model(df_clean, [feature_column], target_column)
        
#         # Display metrics
#         st.write(f"### Model Evaluation Metrics")
#         st.write(f"Mean Squared Error (MSE): {metrics['mse']}")
#         st.write(f"Root Mean Squared Error (RMSE): {metrics['rmse']}")
#         st.write(f"Mean Absolute Error (MAE): {metrics['mae']}")
#         st.write(f"R-squared (R²): {metrics['r_squared']}")
        
#         # Residual Plot
#         st.write("### Residual Plot")
#         residuals = metrics['actual'] - metrics['predicted']
#         fig_residual = plt.figure(figsize=(10, 5))
#         plt.scatter(metrics['predicted'], residuals)
#         plt.axhline(0, color='red', linestyle='--')
#         plt.title('Residual Plot')
#         plt.xlabel('Predicted Sales')
#         plt.ylabel('Residuals')
#         st.pyplot(fig_residual)

#         # Distribution of Residuals
#         st.write("### Distribution of Residuals")
#         fig_residual_dist = plt.figure(figsize=(10, 5))
#         sns.histplot(residuals, bins=30, kde=True)
#         plt.title('Distribution of Residuals')
#         plt.xlabel('Residuals')
#         plt.ylabel('Frequency')
#         st.pyplot(fig_residual_dist)

#         # Actual vs. Predicted Scatter Plot
#         st.write("### Actual vs Predicted Scatter Plot")
#         fig_scatter = plt.figure(figsize=(10, 5))
#         plt.scatter(metrics['actual'], metrics['predicted'], alpha=0.6)
#         plt.plot([metrics['actual'].min(), metrics['actual'].max()], 
#                  [metrics['actual'].min(), metrics['actual'].max()], 
#                  color='red', linestyle='--')  # Diagonal line for reference
#         plt.title('Actual vs Predicted Sales')
#         plt.xlabel('Actual Sales')
#         plt.ylabel('Predicted Sales')
#         st.pyplot(fig_scatter)

#         # Feature Importance Plot (if applicable)
#         if hasattr(model, 'feature_importances_'):
#             st.write("### Feature Importance")
#             importance_df = pd.DataFrame({
#                 'Feature': [feature_column],
#                 'Importance': model.feature_importances_
#             })
#             importance_df = importance_df.sort_values(by='Importance', ascending=False)
#             fig_importance = plt.figure(figsize=(10, 5))
#             sns.barplot(data=importance_df, x='Importance', y='Feature')
#             plt.title('Feature Importance')
#             st.pyplot(fig_importance)

# else:
#     st.write("Select 'Build Sales Forecast Model' from the sidebar to begin.")

# End of Streamlit app

# Footer
st.sidebar.write("---")
st.sidebar.write("Project by `Asif Sayyed`")