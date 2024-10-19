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

def convert_int_to_datetime(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Converts specified integer columns in a DataFrame to datetime format.
    
    Handles three cases:
    1. 8-digit integers in the format 'YYYYMMDD'.
    2. Unix timestamps.
    3. 4-digit integers representing years, converting them to '01-01-{year}'.

    :param df: The input DataFrame containing integer columns to be converted.
    :param columns: A list of column names to be checked and converted to datetime.
    :returns: The modified DataFrame with specified integer columns converted to datetime format.
    :rtype: pd.DataFrame
    """
    for col in columns:
        if col in df.columns and df[col].dtype == 'int64':
            # Create a mask for each case and apply the conversions more efficiently
            yyyymmdd_mask = df[col].between(19000101, 21001231)
            unix_timestamp_mask = df[col].between(0, 2147483647)
            year_mask = df[col].between(1000, 9999)
            
            # Apply conversion only to the masked rows
            df.loc[yyyymmdd_mask, col] = pd.to_datetime(df.loc[yyyymmdd_mask, col], format='%Y%m%d', errors='coerce')
            df.loc[unix_timestamp_mask, col] = pd.to_datetime(df.loc[unix_timestamp_mask, col], unit='s', errors='coerce')
            df.loc[year_mask, col] = pd.to_datetime(df.loc[year_mask, col].astype(str) + '0101', format='%Y%m%d', errors='coerce')
    
    return df
