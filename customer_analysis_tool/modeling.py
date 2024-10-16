import pandas as pd
from .config import Config
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def build_sales_forecast_model(
    df: pd.DataFrame, 
    feature_columns: str, 
    target_column: str
    ) -> tuple[LinearRegression,dict]:
    """
    Builds and evaluates a simple regression model to forecast sales.

    :param df: Input dataset.
    :param feature_columns: List of columns to use as features.
    :param target_column: Column to predict (target variable).
    
    :returns: Trained model.
    :rtype: LinearRegression()
    :returns: Evaluation metrics for the model.
    :rtype: dict
    """
    X = df[feature_columns]
    y = df[target_column]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    metrics = {'mse': mse}
    
    return model, metrics
