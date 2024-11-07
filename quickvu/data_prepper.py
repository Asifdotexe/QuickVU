import pandas as pd
import numpy as np

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

def handle_missing_values(dataframe: pd.DataFrame, method: str = "drop") -> pd.DataFrame:
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