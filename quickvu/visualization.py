import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_sales_by_product(
    df: pd.DataFrame, 
    product_column: str, 
    sales_column: str
) -> plt.Figure:
    """
    Plots total sales by product.
    
    :param df: Input dataset.
    :param product_column: Column representing products.
    :param sales_column: Column representing sales amount.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    
    # Group by product and sum sales
    sales_by_product = df.groupby(product_column)[sales_column].sum().reset_index()
    
    # Check the number of unique products
    if sales_by_product.shape[0] > 10:
        # Take the top 10 products based on sales
        sales_by_product = sales_by_product.nlargest(10, sales_column)

    # Plot the bar chart
    sns.barplot(x=product_column, y=sales_column, data=sales_by_product, ax=ax)
    ax.set_title('Sales by Category')
    ax.set_xlabel(product_column)
    ax.set_ylabel(sales_column)
    
    # Rotate x-axis labels for better visibility if there are many products
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    return fig

def plot_customer_demographics(
    df: pd.DataFrame, 
    customer_column: str, 
    sales_column: str
    ):
    """
    Plots customer demographics such as the number of purchases per customer.
    
    :param df: Input dataset.
    :param customer_column: Column representing customers.
    :param sales_column: Column representing sales amount.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    customer_sales = df.groupby(customer_column)[sales_column].sum().reset_index()
    sns.histplot(customer_sales[sales_column], bins=20, kde=True, ax=ax)
    ax.set_title('Customer Demographics (Purchases per Customer)')
    return fig
