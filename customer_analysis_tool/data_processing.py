import pandas as pd
from .config import Config

def preprocess_data(
    df: pd.DataFrame, 
    column_mapping: dict = None
    ) -> pd.DataFrame:
    """
    Cleans and preprocesses the input dataframe based on column mappings.
    
    :param df: The input dataset.
    :param column_mapping: A dictionary for custom column mappings.

    :returns: Cleaned dataframe.
    :rtype: pd.DataFrame
    """
    if column_mapping is None:
        column_mapping = {
            'customer_id': Config.CUSTOMER_ID,
            'sales_amount': Config.SALES_AMOUNT,
            'purchase_date': Config.PURCHASE_DATE,
            'product_id': Config.PRODUCT_ID,
            'marketing_spend': Config.MARKETING_SPEND
        }

    # Convert purchase date to datetime
    # df[column_mapping['purchase_date']] = pd.to_datetime(
    #     df[column_mapping['purchase_date']], format=Config.DATE_FORMAT, errors='coerce'
    # )

    # Handle missing values
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:  # Check if the column is numeric
            if Config.FILL_MISSING_METHOD == 'mean':
                # Fill missing values with the mean, if the column is numeric
                df[column].fillna(df[column].mean(), inplace=True)
            elif Config.FILL_MISSING_METHOD == 'median':
                # Fill missing values with the median, if the column is numeric
                df[column].fillna(df[column].median(), inplace=True)
            elif Config.FILL_MISSING_METHOD == 'drop':
                # Drop rows with missing values
                df.dropna(subset=[column], inplace=True)
    return df
