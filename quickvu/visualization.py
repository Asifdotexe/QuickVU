import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_metrics_by_category(
    df: pd.DataFrame, 
    category_column: str, 
    numerical_column: str
) -> plt.Figure:
    """
    Plots total metrics by category.
    
    :param df: Input dataset.
    :param category_column: Column representing categorical values.
    :param numerical_column: Column representing numerical values.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    
    # Group by product and sum sales
    metric_by_category = df.groupby(category_column)[numerical_column].sum().reset_index()
    
    # Check the number of unique products
    if metric_by_category.shape[0] > 10:
        # Take the top 10 products based on sales
        metric_by_category = metric_by_category.nlargest(10, numerical_column)

    # Plot the bar chart
    sns.barplot(x=category_column, y=numerical_column, data=metric_by_category, ax=ax)
    ax.set_title('Metrics by Category')
    ax.set_xlabel(category_column)
    ax.set_ylabel(numerical_column)
    
    # Rotate x-axis labels for better visibility if there are many products
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    return fig

def plot_distribution(
    df: pd.DataFrame, 
    categorical_column: str, 
    numerical_column: str
    ):
    """
    Plots customer demographics such as the number of purchases per customer.
    
    :param df: Input dataset.
    :param customer_column: Column representing customers.
    :param sales_column: Column representing sales amount.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    customer_sales = df.groupby(categorical_column)[numerical_column].sum().reset_index()
    sns.histplot(customer_sales[numerical_column], bins=20, kde=True, ax=ax)
    ax.set_title('Histogram Plot')
    return fig
