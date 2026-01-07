import pandas as pd
import numpy as np

def calculate_metrics(returns):
    """
    Compute performance KPIs: Sharpe Ratio and Maximum Drawdown.
    """
    if returns.empty or returns.std() == 0:
        return 0.0, 0.0
        
    # Annualized Sharpe Ratio (assuming 252 trading days)
    sharpe = np.sqrt(252) * returns.mean() / returns.std()
    
    # Calculate Maximum Drawdown (peak to trough decline)
    cum_ret = (1 + returns).cumprod()
    peak = cum_ret.cummax()
    mdd = ((cum_ret - peak) / peak).min()
    
    return round(sharpe, 2), round(mdd * 100, 2)

def apply_sma_strategy(df, fast=20, slow=50):
    """
    Trend Following: Simple Moving Average Crossover logic.
    """
    data = df.copy()
    
    # Calculate technical indicators
    data['Fast_MA'] = data['Price'].rolling(window=fast).mean()
    data['Slow_MA'] = data['Price'].rolling(window=slow).mean()
    
    # Generate Buy (1) and Neutral (0) signals
    data['Signal'] = 0
    data.loc[data['Fast_MA'] > data['Slow_MA'], 'Signal'] = 1
    
    # Backtest returns based on signals
    data['Returns'] = data['Price'].pct_change() * data['Signal'].shift(1)
    data['Cumulative'] = (1 + data['Returns'].fillna(0)).cumprod()
    
    return data

def apply_rsi_strategy(df, window=14, low=30, high=70):
    """
    Mean Reversion: Relative Strength Index (RSI) strategy.
    """
    data = df.copy()
    
    # Standard RSI calculation
    delta = data['Price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Generate signals: Buy when oversold (<30), Sell when overbought (>70)
    data['Signal'] = 0
    data.loc[data['RSI'] < low, 'Signal'] = 1 
    data.loc[data['RSI'] > high, 'Signal'] = -1 
    
    # Strategy performance calculation
    data['Returns'] = data['Price'].pct_change() * data['Signal'].shift(1)
    data['Cumulative'] = (1 + data['Returns'].fillna(0)).cumprod()
    
    return data