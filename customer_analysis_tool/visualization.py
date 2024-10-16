import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_sales_by_product(
    df: pd.DataFrame, 
    product_column: str, 
    sales_column: str
    ):
    """
    Plots total sales by product.
    
    :param df: Input dataset.
    :param product_column: Column representing products.
    :param sales_column: Column representing sales amount.
    
    :returns: Matplotlib figure object
    """
    fig, ax = plt.subplots()
    sales_by_product = df.groupby(product_column)[sales_column].sum().reset_index()
    sns.barplot(x=product_column, y=sales_column, data=sales_by_product, ax=ax)
    ax.set_title('Sales by Product')
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
