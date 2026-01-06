import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.quant_a.data_handler import get_historical_data, get_live_price
from src.quant_a.strategy_engine import run_buy_and_hold_strategy, run_ma_crossover_strategy, calculate_performance_metrics
from src.quant_b.portfolio_manager import get_portfolio_data, calculate_portfolio_metrics
import numpy as np

st.set_page_config(page_title="Multi-Quant Finance Platform", layout="wide")

# Navigation
tab1, tab2 = st.tabs(["🚀 NVIDIA Analysis (Module A)", "💼 Portfolio Management (Module B)"])

# ==========================================
# MODULE A: SINGLE ASSET (YOUR PART)
# ==========================================
with tab1:
    st.header("NVIDIA Quantitative Analysis")
    # ... (On garde ton code précédent ici) ...
    ticker = "NVDA"
    data_a = get_historical_data(ticker, "1y")
    if not data_a.empty:
        st.line_chart(data_a)

# ==========================================
# MODULE B: MULTI-ASSET (COLLEAGUE'S PART)
# ==========================================
with tab2:
    st.header("Multi-Asset Portfolio Optimization")
    
    # User inputs for Part B
    assets = st.multiselect("Select Assets", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"], default=["AAPL", "MSFT", "TSLA"])
    
    if len(assets) >= 2:
        data_b = get_portfolio_data(assets)
        
        # Simple Equal Weighting for now
        weights = np.array([1/len(assets)] * len(assets))
        
        results = calculate_portfolio_metrics(data_b, weights)
        
        # Display Volatility
        st.metric("Portfolio Annualized Volatility", f"{results['volatility']*100:.2f}%")
        
        # Correlation Heatmap
        st.subheader("Asset Correlation Matrix")
        st.write(results['correlation'])
        
        # Cumulative Performance
        st.subheader("Portfolio Cumulative Return")
        st.line_chart(results['cumulative'])
    else:
        st.warning("Please select at least 2 assets to analyze correlation and portfolio performance.")