import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_summary_statistics(df: pd.DataFrame):
    """
    Generates and returns summary statistics for the dataframe.
    
    :param df: Input dataset.
    
    :returns: Summary statistics.
    :rtype: pd.DataFrame
    """
    return df.describe()

def plot_sales_trends(
    df: pd.DataFrame, 
    date_column: str, 
    sales_column: str
    ):
    """
    Plots sales trends over time.

    :param df: Input dataset.
    :param date_column: The column representing dates.
    :param sales_column: The column representing sales amount.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    df.groupby(date_column)[sales_column].sum().plot(ax=ax)  # Group by date_column without .dt
    ax.set_title('Sales Trends Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Sales Amount')
    return fig


def plot_correlation_matrix(df: pd.DataFrame):
    """
    Plots a correlation matrix of the dataset.
    
    :param df: Input dataset.
    
    :returns: Matplotlib figure object
    """
    numeric_df = df.select_dtypes(include=['number'])
    corr = numeric_df.corr()
    fig, ax = plt.subplots()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr, annot=False, cmap='coolwarm', ax=ax, square=True, center=0)
    ax.set_title('Correlation Matrix')
    return fig
