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