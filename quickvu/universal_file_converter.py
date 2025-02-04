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


