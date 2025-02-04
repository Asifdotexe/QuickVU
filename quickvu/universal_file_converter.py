"""
This script is for a universal file converter, that can convert any file
into any other compatible type of file
"""

import pandas as pd

def detect_file_type(file_name: str) -> tuple[str, str]:
    """This function takes the file name and extracts the extension

    :param file_name: name of the input file
    :type file_name: str
    """
    current_file_name, extension = file_name.split('.')
    return current_file_name, extension.lower()

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

def get_conversion_options(file_type: str):
    """
    This function figures out the compatible datatypes we can convert it in
    """
    options = {
        "csv": ["json", "xlsx", "parquet"],
        "xlsx": ["csv", "json", "parquet"],
        "json": ["csv", "xlsx"],
        "parquet": ["csv", "xlsx"]
    }
    return options.get(file_type, [])

def convert_file(df: pd.DataFrame, convert_to: str, current_file_name: str):
    """
    This function is responsible for changing the datatype to the one specified in
    `convert_to` parameter
    """
    output_path = f"converted_{current_file_name}.{convert_to}"
    if convert_to == "csv":
        df.to_csv(output_path, index=False)
    elif convert_to == "xlsx":
        df.to_excel(output_path, index=False)
    elif convert_to == "json":
        df.to_json(output_path, orient="records", indent=2)
    elif convert_to == "parquet":
        df.to_parquet(output_path)
    return output_path