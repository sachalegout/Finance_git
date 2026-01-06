import yfinance as yf
import pandas as pd

# On définit le ticker pour NVIDIA
TICKER = "NVDA"

def get_nvidia_data(period="1y"):
    """
    Récupère les données historiques de NVIDIA.
    Period peut être '1mo', '6mo', '1y', etc.
    """
    try:
        # Récupération des données via yfinance
        df = yf.download(TICKER, period=period, interval="1d", progress=False)
        
        # On nettoie un peu pour n'avoir que le prix de clôture
        if not df.empty:
            # On garde seulement la colonne 'Close'
            df = df[['Close']]
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        return pd.DataFrame()

def get_current_price():
    """Récupère le tout dernier prix pour l'affichage temps réel."""
    try:
        ticker_obj = yf.Ticker(TICKER)
        # On essaie de choper le prix actuel
        price = ticker_obj.fast_info['lastPrice']
        return price
    except:
        return None