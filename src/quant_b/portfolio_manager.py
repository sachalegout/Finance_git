import pandas as pd
import numpy as np
import yfinance as yf

def get_portfolio_data(tickers, period="1y"):
    """
    Fetch historical close prices for multiple assets.
    Requirement: Quant B - Multi-asset support.
    """
    try:
        data = yf.download(tickers, period=period, interval="1d", progress=False)
        
        # Extract only Close column and handle potential MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data = data['Close']
        else:
            data = data[['Close']]
            
        return data.dropna()
    except Exception as e:
        print(f"Error loading portfolio data: {e}")
        return pd.DataFrame()

def calculate_portfolio_metrics(data, weights, rf_rate=0.0):
    """
    Compute portfolio metrics.
    """
    returns = data.pct_change().dropna()
    port_returns = returns.dot(weights)
    cum_returns = (1 + port_returns).cumprod()
    
    # Annualized Volatility
    cov_matrix = returns.cov() * 252
    port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    port_volatility = np.sqrt(port_variance)
    
    daily_rf = rf_rate / 252
    
    # Sharpe Ratio = (Return - RiskFree) / Volatility
    avg_excess_return = port_returns.mean() - daily_rf
    std_return = port_returns.std()
    
    # Annualize the result
    sharpe = (avg_excess_return / std_return) * np.sqrt(252) if std_return != 0 else 0
    
    # Diversification Benefit
    individual_vols = returns.std() * np.sqrt(252)
    weighted_avg_vol = np.dot(individual_vols, weights)
    div_benefit = weighted_avg_vol - port_volatility
    
    corr_matrix = returns.corr()
    individual_cum_returns = (1 + returns).cumprod()
    
    return {
        "returns": port_returns,
        "cumulative": cum_returns,
        "volatility": round(port_volatility, 4),
        "sharpe": round(sharpe, 2),
        "div_benefit": round(div_benefit, 4),
        "correlation": corr_matrix,
        "individual_cum_returns": individual_cum_returns
    }