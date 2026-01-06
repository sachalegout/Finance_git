import yfinance as yf
import pandas as pd

def get_historical_data(ticker, period="1y"):
    """
    Fetches historical data using the Ticker object.
    This method returns a cleaner DataFrame that avoids MultiIndex errors.
    """
    try:
        # Using Ticker().history is safer for single stocks than yf.download
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if not df.empty:
            # The .history() method returns columns like ['Open', 'Close', ...] 
            # so we can simply select 'Close'.
            return df[['Close']]
            
        return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching history: {e}")
        return pd.DataFrame()

def get_live_price(ticker):
    """
    Fetches the live price.
    Accepts 'ticker' from app.py.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        # fast_info is the modern way to get the latest price
        price = ticker_obj.fast_info['lastPrice']
        return price
    except:
        return None