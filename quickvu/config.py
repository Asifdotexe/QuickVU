import os
from dotenv import load_dotenv
import google.generativeai as genai

class Config:
    # Constants for data columns
    CUSTOMER_ID = 'customer_id'
    SALES_AMOUNT = 'sales_amount'
    PURCHASE_DATE = 'purchase_date'
    PRODUCT_ID = 'product_id'
    MARKETING_SPEND = 'marketing_spend'

    # Date format for parsing dates
    DATE_FORMAT = '%Y-%m-%d' 

    # Method for handling missing data
    FILL_MISSING_METHOD = 'mean'

    # Modelling parameters
    TARGET_VARIABLE = 'sales_amount'
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
