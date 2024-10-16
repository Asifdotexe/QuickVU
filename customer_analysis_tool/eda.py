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
    df.groupby(df[date_column].dt.to_period('M'))[sales_column].sum().plot(ax=ax)
    ax.set_title('Sales Trends Over Time')
    return fig

def plot_correlation_matrix(df: pd.DataFrame):
    """
    Plots a correlation matrix of the dataset.
    
    :param df: Input dataset.
    
    :returns: Matplotlib figure object
    """
    corr = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    return fig
