import pandas as pd
import numpy as np

def calculate_performance_metrics(returns):
    """Compute Sharpe Ratio and Max Drawdown metrics."""
    if returns.empty or returns.std() == 0:
        return 0.0, 0.0
    
    # Annualized Sharpe Ratio (using 0 as risk-free rate)
    sharpe = np.sqrt(252) * (returns.mean() / returns.std())
    
    # Max Drawdown calculation
    cum_wealth = (1 + returns).cumprod()
    peak = cum_wealth.cummax()
    drawdown = (cum_wealth - peak) / peak
    max_dd = drawdown.min()
    
    return round(float(sharpe), 2), round(float(max_dd), 2)

def run_buy_and_hold_strategy(prices):
    """Standard long-term investment strategy."""
    df = pd.DataFrame(prices)
    df.columns = ['Price']
    df['Returns'] = df['Price'].pct_change()
    df['Cumulative_Return'] = (1 + df['Returns']).cumprod()
    return df

def run_ma_crossover_strategy(prices, fast_ma=20, slow_ma=50):
    """Moving Average Crossover momentum strategy."""
    df = pd.DataFrame(prices)
    df.columns = ['Price']
    
    # Calculate moving averages
    df['Fast_MA'] = df['Price'].rolling(window=fast_ma).mean()
    df['Slow_MA'] = df['Price'].rolling(window=slow_ma).mean()
    
    # Trading signals: 1 when short MA is above long MA
    df['Signal'] = 0
    df.loc[df['Fast_MA'] > df['Slow_MA'], 'Signal'] = 1
    
    # Calculate returns (shifting signal to avoid look-ahead bias)
    df['Returns'] = df['Price'].pct_change() * df['Signal'].shift(1)
    df['Cumulative_Return'] = (1 + df['Returns']).cumprod()
    
    return df