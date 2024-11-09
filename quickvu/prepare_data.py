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
    # we want the script to handle the datatypes gracefully without causing errors
    numerical_columns = dataframe.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = dataframe.select_dtypes(exclude=[np.number]).columns.tolist()

    if method == "drop":
        # dropping the missing values without any caveats
        dataframe = dataframe.dropna()
        
    elif method == "mean":
        # imputing numerical columns with mean and categorical with mode
        dataframe[numerical_columns] = dataframe[numerical_columns].fillna(dataframe[numerical_columns].mean())
        for column in categorical_columns:
            dataframe[column] = dataframe[column].fillna(dataframe[column].mode()[0])
            
    elif method == "median":
        # Impute numerical columns with median and categorical with mode
        dataframe[numerical_columns] = dataframe[numerical_columns].fillna(dataframe[numerical_columns].median())
        for column in categorical_columns:
            dataframe[column] = dataframe[column].fillna(dataframe[column].mode()[0])  # Using mode for categorical columns
            
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
        if dtype == 'datetime':
            dataframe[column] = pd.to_datetime(dataframe[column], errors='coerce')
        else:
            dataframe[column] = dataframe[column].astype(dtype)
    return dataframe

def detech_outliers(
        dataframe: pd.DataFrame, 
        method: str = "iqr",
        threshold: float = 1.5,
        columns: list = None  # Accept a list of columns instead of a single column
    ) -> pd.DataFrame:
    """
    Detect outliers using the specified method.

    :param dataframe: The DataFrame to detect outliers in.
    :type dataframe: pd.DataFrame
    :param method: Method to detect outliers. Options are `iqr` or `zscore`.
    :type method: str, optional
        Default is `iqr`.
    :param threshold: The threshold to determine outliers based on the chosen method.
    :type threshold: float, optional
        Default is 1.5.
    :param columns: List of columns to detect outliers in. If None, detects outliers in all numerical columns.
    :type columns: list, optional

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
    # defining a list of numerical values
    # Determine which columns to use: the specified column or all numerical columns
    if columns is None:
        columns = dataframe.select_dtypes(include=[np.number]).columns.tolist()
        
    if method == "iqr":
        Q1 = dataframe[columns].quantile(0.25)
        Q3 = dataframe[columns].quantile(0.75)
        IQR = Q3 - Q1
        outliers = (dataframe[columns] < (Q1 - threshold * IQR)) | \
                   (dataframe[columns] > (Q3 + threshold * IQR))
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
        z_scores = np.abs(dataframe[columns].apply(zscore))
        outliers = z_scores > threshold
    else:
        raise ValueError("Invalid method for detecting outliers. Choose 'iqr' or 'zscore'.")
            
    # adding the outliers into dataframe to create flags
    for column in columns:
        dataframe[f"{column}_outliers"] = outliers[column]
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

def manipulate_columns(
        dataframe: pd.DataFrame, 
        column_operations: dict
    ) -> pd.DataFrame:
    """Perform various column manipulation like renaming or adding new columns.
    
    :param dataframe: The DataFrame to manipulate columns.
    :type dataframe: pd.DataFrame
    :param column_operations: A dictionary containing operations to perform on columns.
    :type column_operations: dict\n
    Example: `{'rename': {'old_name': 'new_name'}, 'add': {'new_column': lambda x: x['column1'] + x['column2']}}`
    
    
    :return: DataFrame with manipulated columns.
    :rtype: pd.DataFrame
    """
    if 'rename' in column_operations:
        dataframe = dataframe.rename(column=column_operations['rename'])
    if 'add' in column_operations:
        for new_column, func in column_operations['add'].items():
            dataframe[new_column] = dataframe.apply(func, axis=1)
    return dataframe

def filter_rows(
        dataframe: pd.DataFrame, 
        filter_conditions: dict,
    ) -> pd.DataFrame:
    """Filter rows based on specified conditions
    
    :param dataframe: The DataFrame to filter rows from.
    :type dataframe: pd.DataFrame
    :param filter_conditions: A dictionary containing conditions for filtering rows.
    :type filter_conditions: dict\n
        Example: `{'column1': 'value1', 'column2': 'value2'}`
        
    :return: Filtered DataFrame
    :rtype: pd.DataFrame
    """
    for column, value in filter_conditions.items():
        dataframe = dataframe[dataframe[column] == value]
    return dataframe

def export_data(
        dataframe: pd.DataFrame,
        file_name: str ='cleaned_data.csv',
    ) -> str:
    """Export the cleaned DataFrame to a CSV file.
    
    :param dataframe: The DataFrame to export.
    :type dataframe: pd.DataFrame
    :param file_name: The name of the file to export the data to.
    :type file_name: str, optional
        Default is `cleaned_data.csv`
        
    :return: Path to the saved CSV file
    :rtype: str
    """
    dataframe.to_csv(file_name, index=False)
    return f'Data exported to {file_name}'