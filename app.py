import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

from quickvu.config import Config
from quickvu import data_processing, eda, visualization
from quickvu import gemini

sns.set_style('whitegrid')

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
    .warning-message {
        color: #0b78ee;
        font-size: 16px;
        font-weight: 500;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">QuickVU: Adhoc Data Analysis Tool</h1>', unsafe_allow_html=True)
st.markdown("""
Quick VU (Quick Visual Understanding) is a no-code data visualization and analysis tool. Designed with simplicity in mind, 
Quick VU helps users explore datasets with ease. Just upload your data, select your analysis options, and let Quick VU guide you 
through insights and visualizations.
""")

st.sidebar.image('./dataset/logo.png', use_column_width=True)


st.sidebar.markdown('<h3 class="side-header">Upload your Dataset</h3>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"], help="Upload your dataset in CSV format for analysis.")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown('<h2 class="sub-header">Dataset Preview</h2>', unsafe_allow_html=True)
    st.write(df.head(10))
    
    columns = df.columns.tolist()
    column_types = df.dtypes

    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    st.sidebar.markdown('<h3 class="side-header">Select Columns for Analysis</h3>', unsafe_allow_html=True)
    selected_categorical = st.sidebar.multiselect("Select Categorical Columns", categorical_columns, help="Choose columns with categorical data like 'Product Type', 'Category', etc.")
    selected_numerical = st.sidebar.multiselect("Select Numerical Columns", numerical_columns, help="Select columns with numerical data like 'Sales Amount', 'Profit', etc.")
    selected_datetime = st.sidebar.multiselect("Select Date/Time Columns", columns, help="Choose date columns for time-based analysis.")
    
    # Convert integer columns to datetime
    df = data_processing.convert_int_to_datetime(df, selected_datetime)

    st.sidebar.markdown('<h3 class="side-header">Preprocessing Options</h3>', unsafe_allow_html=True)
    missing_value_option = st.sidebar.selectbox(
        "How do you want to handle missing values?",
        ("Fill with Mean", "Fill with Median", "Drop Missing Rows"),
        help="Choose how to handle missing values in your dataset."
    )
    
    if missing_value_option == "Fill with Mean":
        Config.FILL_MISSING_METHOD = 'mean'
    elif missing_value_option == "Fill with Median":
        Config.FILL_MISSING_METHOD = 'median'
    else:
        Config.FILL_MISSING_METHOD = 'drop'

    st.markdown('<h2 class="sub-header">Preprocessed Dataset</h2>', unsafe_allow_html=True)
    df_clean = data_processing.preprocess_data(df)
    st.write(df_clean.head())

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.sidebar.markdown('<h3 class="side-header">Exploratory Data Analysis</h3>', unsafe_allow_html=True)
    
    if st.sidebar.checkbox("Show Summary Statistics", help="Display summary statistics such as mean, median, and standard deviation for numerical columns."):
        st.markdown('<h2 class="sub-header">Summary Statistics</h2>', unsafe_allow_html=True)
        st.write("Numerical:",eda.generate_summary_statistics(df_clean))
        st.write("Categorical:",eda.generate_object_summary_statistics(df_clean))

    if st.sidebar.checkbox("Show Correlation Matrix", help="Display a correlation matrix for selected numerical columns."):
        st.markdown('<h2 class="sub-header">Correlation Matrix</h2>', unsafe_allow_html=True)
        
        if selected_numerical:
            df_numerical = df_clean[selected_numerical]
            correlation_matrix = df_numerical.corr()

            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8}, ax=ax)
            ax.set_title('Correlation Matrix of Selected Numerical Columns', fontsize=16, fontweight='bold', color="#333")
            st.pyplot(fig)

            # Explanation Section
            with st.expander("Need Help Understanding the Correlation Matrix?"):
                if st.button("Explain Correlation Matrix"):
                    corr_matrix_str = correlation_matrix.to_string()  # Convert the correlation matrix to string
                    with st.spinner("Generating explanation..."):
                        explanation = gemini.explain_correlation_matrix(corr_matrix_str)
                    st.markdown('<h2 class="sub-header">Explanation</h2>', unsafe_allow_html=True)
                    st.info(explanation, icon="💡")
        else:
            st.markdown(
                '<p class="warning-message">Please select at least one numerical column to view the correlation matrix.</p>', 
                unsafe_allow_html=True
            )

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Step 6: Visualization
    st.sidebar.markdown('<h3 class="side-header">Data Visualization</h3>', unsafe_allow_html=True)
    
    if st.sidebar.checkbox("Plot Sales by Product", help="Plot a bar chart to visualize sales by product."):
        st.markdown('<h2 class="sub-header">Sales by Product</h2>', unsafe_allow_html=True)
        if selected_categorical and selected_numerical:
            product_col = st.sidebar.selectbox("Select Product Column", selected_categorical, key="product_col", help="Select a categorical column representing products.")
            sales_col = st.sidebar.selectbox("Select Sales Amount Column", selected_numerical, key="sales_col", help="Select a numerical column representing sales amounts.")
            fig = visualization.plot_sales_by_product(df_clean, product_col, sales_col)
            st.pyplot(fig)
        else:
            st.markdown('<p class="warning-message">Please select both a Categorical and a Numerical column for this analysis.</p>', unsafe_allow_html=True)

    # Plot by dates
    if st.sidebar.checkbox("Plot Sales Trends", help="Plot sales trends over time based on selected columns"):
        st.write("## Sales Trends Over Time")

        datetime_columns = df_clean.select_dtypes(include=['datetime64[ns]', 'object']).columns.tolist()

        if datetime_columns and numerical_columns:
            date_col = datetime_columns[0] if len(datetime_columns) == 1 else st.sidebar.selectbox("Select Purchase Date Column", datetime_columns)
            amount_col = st.sidebar.selectbox("Select Sales Amount Column", selected_numerical)

            if date_col and amount_col:
                df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
                df_clean = df_clean.dropna(subset=[date_col, amount_col])  # Drop rows with NaT or NaN values

                if not df_clean.empty:  # Check if the DataFrame is not empty after dropping NaNs
                    fig = eda.plot_sales_trends(df_clean, date_col, amount_col)
                    st.pyplot(fig)
                else:
                    st.warning("No valid data available for the selected columns.")
            else:
                st.warning("Please ensure both a valid date column and a sales amount column are selected.")
        else:
            st.warning("Please ensure your dataset contains both Date/Time and Numerical columns for this analysis.")


# Footer
st.sidebar.write("---")
st.sidebar.write("Project by `Asif Sayyed`")
