import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_prices(df, days=5):
    """
    ML model for price trend prediction.
    Requirement: Optional Bonus - Predictive model.
    """
    # Prepare historical data for the model
    df_reset = df.reset_index()
    X = np.array(df_reset.index).reshape(-1, 1) 
    y = df_reset['Price'].values               
    
    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future time index for the next 5 days
    future_index = np.array(range(len(df_reset), len(df_reset) + days)).reshape(-1, 1)
    
    # Forecast future values based on current trend
    predictions = model.predict(future_index)
    
    return predictions