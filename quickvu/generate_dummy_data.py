import pandas as pd
import numpy as np

np.random.seed(0)

def generate_test_data(num_rows=100):
    """Generates a DataFrame of dummy employee data with specified attributes and introduces some NaN values and outliers.

    :param num_rows: The number of rows to generate in the DataFrame, defaults to 100.
    :type num_rows: int, optional

    :return: A DataFrame containing synthetic employee data with columns for ID, Name, Age, Salary, Gender, Department, Joining_Date, Performance_Score, and Comments.
    :rtype: pandas.DataFrame
    """
    data = {
        'ID': np.arange(1, num_rows + 1),
        'Name': [f'Person_{i}' for i in range(1, num_rows + 1)],
        'Age': np.random.randint(18, 60, size=num_rows).astype(float),  # Random ages between 18 and 60
        'Salary': np.random.normal(50000, 12000, size=num_rows),  # Normally distributed salary
        'Gender': np.random.choice(['Male', 'Female'], size=num_rows),
        'Department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing'], size=num_rows),
        'Joining_Date': pd.to_datetime('2020-01-01') + pd.to_timedelta(np.random.randint(0, 365, num_rows), unit='D'),
        'Performance_Score': np.random.normal(70, 10, size=num_rows),  # Normally distributed performance score
        'Comments': ['Good performance' if i % 2 == 0 else 'Needs improvement' for i in range(num_rows)]
    }
    
    # Introduce some NaN values
    data['Age'][np.random.choice(num_rows, 10, replace=False)] = np.nan
    data['Salary'][np.random.choice(num_rows, 5, replace=False)] = np.nan
    data['Comments'] = pd.Series(['Good performance' if i % 2 == 0 else 'Needs improvement' for i in range(num_rows)])

    # Use .iloc to assign None to random rows in 'Comments' based on their integer position, 
    # as direct indexing with a list of integers can cause errors in pandas.
    random_indices = np.random.choice(num_rows, 8, replace=False)
    data['Comments'].iloc[random_indices] = None

    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add some outliers in the 'Salary' and 'Performance_Score' columns
    df.loc[np.random.choice(num_rows, 3, replace=False), 'Salary'] = 200000  # Very high salaries as outliers
    df.loc[np.random.choice(num_rows, 3, replace=False), 'Performance_Score'] = 5  # Very low performance scores as outliers
    
    return df

dummy_data = generate_test_data(100)
dummy_data.to_csv(r"..\dataset\prepper_test_data.csv", index=False)
