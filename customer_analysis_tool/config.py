# config.py

class Config:
    CUSTOMER_ID = 'customer_id'
    SALES_AMOUNT = 'sales_amount'
    PURCHASE_DATE = 'purchase_date'
    PRODUCT_ID = 'product_id'
    MARKETING_SPEND = 'marketing_spend'


    DATE_FORMAT = '%Y-%m-%d' 
    FILL_MISSING_METHOD = 'mean'

    # Modelling parameters
    TARGET_VARIABLE = 'sales_amount'
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
