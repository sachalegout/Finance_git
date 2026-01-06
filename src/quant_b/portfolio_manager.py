import pandas as pd
import numpy as np
import yfinance as yf

def get_portfolio_data(tickers, period="1y"):
    """Fetch historical data for multiple assets."""
    try:
        data = yf.download(tickers, period=period, interval="1d", progress=False)['Close']
        return data.dropna()
    except Exception as e:
        print(f"Error fetching portfolio data: {e}")
        return pd.DataFrame()

def calculate_portfolio_metrics(data, weights):
    """Compute portfolio returns, volatility and correlation."""
    returns = data.pct_change().dropna()
    port_returns = returns.dot(weights)
    cum_returns = (1 + port_returns).cumprod()
    
    # Annualized Volatility: sigma_p = sqrt(w.T * Cov * w) * sqrt(252)
    cov_matrix = returns.cov() * 252
    port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    port_volatility = np.sqrt(port_variance)
    
    # Correlation Matrix
    corr_matrix = returns.corr()
    
    return {
        "returns": port_returns,
        "cumulative": cum_returns,
        "volatility": round(port_volatility, 4),
        "correlation": corr_matrix
    }