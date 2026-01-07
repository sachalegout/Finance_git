import yfinance as yf
import pandas as pd

def get_historical_data(ticker="NVDA", period="1y"):
    """
    Download and clean market data from Yahoo Finance.
    """
    try:
        data = yf.download(ticker, period=period, interval="1d", progress=False)
        
        if data.empty:
            return pd.DataFrame()

        # Handle yfinance MultiIndex column issue
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Extract closing price and rename column
        df = data[['Close']].copy()
        df.columns = ['Price']
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()