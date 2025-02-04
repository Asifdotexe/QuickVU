"""
This script is for a universal file converter, that can convert any file
into any other compatible type of file
"""

import os
import json
import pandas as pd
import pyarrow.parquet as pq

def detect_file_type(file_name: str) -> str:
    """This function takes the file name and extracts the extension

    :param file_name: name of the input file
    :type file_name: str
    """
    extension = file_name.split('.')[-1].lower()
    return extension

def read_file(uploaded_file, file_type):
    """This function reads the input file and based on the datatype
    reads the file into a dataframe
    """
    if file_type == "csv":
        return pd.read_csv(uploaded_file)
    elif file_type in ["xls", "xlsx"]:
        return pd.read_excel(uploaded_file)
    elif file_type == "json":
        return pd.read_json(uploaded_file, orient="records")
    elif file_type == "parquet":
        return pd.read_parquet(uploaded_file)
    else:
        return None
