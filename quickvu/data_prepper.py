import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def get_data_overview(dataframe: pd.DataFrame) -> dict:
    """Get an overview of the data including basic information and sample rows.
    
    :param dataframe: The DataFrame to explore.
    :type dataframe: pd.DataFrame
    
    :return: Summary of data types, shape, and the first few rows of the dataframe.
    :rtype: dict
    """
    data_overview = {
        "shape": dataframe.shape,
        "columns": dataframe.columns.tolist(),
        "data_types": dataframe.dtypes.to_dict(),
        "sample_rows": dataframe.head().to_dict(orient="records"),
    }
    return data_overview

def handle_missing_values(
        dataframe: pd.DataFrame, 
        method: str = "drop"
    ) -> pd.DataFrame:
    """Handle missing values in the dataset based on the chosen method.
    
    :param dataframe: The Dataframe to handle missing values for.
    :type dataframe: pd.DataFrame
    :param method: The method handle missing values. Options are `drop`, `mean`, or `median`.
    :type method: str, optional
        Default is `drop`
    
    :return: The DataFrame with missing values handled.
    :rtype: pd.DataFrame
    """
    if method == "drop":
        dataframe = dataframe.dropna()
    elif method == "mean":
        dataframe = dataframe.fillna(dataframe.mean())
    elif method == "median":
        dataframe = dataframe.fillna(dataframe.median())
    else:
        raise ValueError("Invalid method for handling missing values. Choose 'drop', 'mean', or 'median'.")
    return dataframe

def convert_data_types(
        dataframe: pd.DataFrame, 
        column_types: dict
    ) -> pd.DataFrame:
    """Convert columns to specific data types.
    
    :param dataframe: The DataFrame to convert column types.
    :type dataframe: pd.DataFrame
    :param column_types: A dictionary where keys are column names and values are target data types.
    :type column_types: dict
    
    :return: DataFrame with updated data types.
    :rtype: pd.DataFrame
    """
    for column, dtype in column_types.items():
        dataframe[column] = dataframe[column].astype(dtype)
    return dataframe

def detech_outliers(
        dataframe: pd.DataFrame, 
        numerical_columns: list, 
        method: str = "iqr",
        threshold: float = 1.5
    ) -> pd.DataFrame:
    """
    Detect outliers using the specified method.

    :param dataframe: The DataFrame to detect outliers in.
    :type dataframe: pd.DataFrame
    :param numerical_columns: List of numerical columns to check for outliers.
    :type numerical_columns: list
    :param method: Method to detect outliers. Options are `iqr` or `zscore`.
    :type method: str, optional
        Default is `iqr`.
    :param threshold: The threshold to determine outliers based on the chosen method.
    :type threshold: float, optional
        Default is 1.5.

    :return: DataFrame with outliers flagged.
    :rtype: pd.DataFrame
    """
    # Interquartile Range (IQR) is a statistical measure used to identify outliers in a dataset.
    # It is the range between the 1st quartile (Q1) and the 3rd quartile (Q3), where:
    
    # - Q1 (the 1st quartile) is the value below which 25% of the data falls.
    # - Q3 (the 3rd quartile) is the value below which 75% of the data falls.
    
    # The IQR is calculated as: IQR = Q3 - Q1
    
    # Outliers are considered any data points that fall below: 
    # - Lower bound = Q1 - 1.5 * IQR
    # - Upper bound = Q3 + 1.5 * IQR
    
    # Here is a basic diagram of the IQR:
    
    #       |---------|---------|---------|---------|---------|
    #  ---- Q1      Median    Q3       Upper Bound    Lower Bound
    
    # Anything outside the "lower bound" and "upper bound" are considered outliers
    if method == "iqr":
        # storing the 1st quantile and 3rd quantile values
        Q1 = dataframe[numerical_columns].quantile(0.25)
        Q3 = dataframe[numerical_columns].quantile(0.75)
        # calculating the interquartile range
        IQR = Q3 - Q1
        # filtering and storing the outlier data
        outliers = (
            (dataframe[numerical_columns] < (Q1 - threshold * IQR)) |
            (dataframe[numerical_columns] < (Q3 + threshold * IQR))
        )
    # The Z-score measures how far a data point is from the mean in terms of standard deviations.
    # Formula: Z = (X - μ) / σ
    # - X is the data point
    # - μ (mu) is the mean
    # - σ (sigma) is the standard deviation
    
    # Z-score interpretation:
    # - Z = 0: data point is at the mean
    # - Z > 0: data point is above the mean
    # - Z < 0: data point is below the mean
    
    # Example diagram:
    #         |-----|-----|-----|-----|-----|-----|
    # Z-score   -3    -2    -1    0     1     2     3
    #         Below mean       Mean        Above mean
    elif method == "zscore":
        z_score = np.abs(zscore[dataframe[numerical_columns]])
        outliers = z_score > threshold
    else:
        raise ValueError("Invalid method for detecting outliers. Choose 'iqr' or 'zscore'.")
            
    # adding the outliers into dataframe to create flags
    dataframe["outliers"] = outliers.any(axis=1)
    return dataframe

def clean_text_data(
        dataframe: pd.DataFrame, 
        text_columns: list
    ) -> pd.DataFrame:
    """Clean text columns by removing extra spaces and non-alphanumeric characters.
    
    :param dataframe: The DataFrame containing text columns.
    :type dataframe: pd.DataFrame
    :param text_columns: List of columns to clean.
    :type text_columns: list
    
    :return: DataFrame with cleaned text data.
    :rtype: pd.DataFrame
    """
    for columns in text_columns:
        dataframe[columns] = dataframe[columns].str.strip()\
                                .str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
    return dataframe

def remove_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from a DataFrame.
    
    :param dataframe: The DataFrame to remove duplicates from.
    :type dataframe: pd.DataFrame
    
    :return: DataFrame with duplicate rows removed.
    :rtype: pd.DataFrame
    """
    dataframe.drop_duplicates(inplace=True)
    return dataframe

def scale_data(
        dataframe: pd.DataFrame,
        numerical_columns: list,
        method: str = "standarize"
    ) -> pd.DataFrame:
    """Scale numerical data to a specified range or distribution.
    
    :param dataframe: The DataFrame containing numerical columns.
    :type dataframe: pd.DataFrame
    :param numerical_columns: List of numerical columns to scale.
    :type numerical_columns: list
    :param method: Method to scale the data. Options are `standarize` (z-score) or `minmax` (min-max).
    :type method: str, optional
        Default is `standardize`.
        
    :return: Scaled DataFrame
    :rtype: pd.DataFrame
    """
    if method == "standarize":
        scaler = StandardScaler()
    elif method == "normalize":
        scaler = MinMaxScaler()
    else:
        raise ValueError("Invalid method for scaling data. Choose 'standarize' or 'minmax'.")
    
    dataframe[numerical_columns] = scaler.fit_transform(dataframe[numerical_columns])
    return dataframe

def standardize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names by converting them to lowercase and removing spaces.
    
    :param dataframe: The DataFrame to standardize column names.
    :type dataframe: pd.DataFrame
    
    :return: DataFrame with standardized column names.
    :rtype: pd.DataFrame
    """
    dataframe.columns = (
        dataframe.columns
        .str.strip()                                  # removing leading and replacing whitespaces 
        .str.lower()                                  # convert to lowercase
        .str.replace(' ', '_', regex=False)           # replacing spaces with underscores
        .str.replace('[^a-zA-Z0-9_]', '', regex=True) # remove non-alphanumeric characters
    )
    return dataframe