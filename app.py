import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from src.quant_a.data_handler import get_historical_data
from src.quant_a.strategy_engine import apply_sma_strategy, apply_rsi_strategy, calculate_metrics
from src.quant_a.models import forecast_prices
from src.quant_b.portfolio_manager import get_portfolio_data, calculate_portfolio_metrics

st.set_page_config(
    page_title="AlphaQuant Institutional Terminal",
    layout="wide",
    page_icon="💹"
)


st.sidebar.title("Global Settings")


horizon = st.sidebar.select_slider(
    "Select Analysis Horizon", 
    options=["3mo", "6mo", "1y", "2y", "5y"], 
    value="1y"
)

st.sidebar.markdown("---")


st.sidebar.title("Risk-Free Settings")
rf_input = st.sidebar.slider("Annual Risk-Free Rate (%)", 0.0, 10.0, 2.0, 0.1)
rf_rate = rf_input / 100 

st.sidebar.markdown("---")


st.sidebar.title("Strategy Parameters")
strategy_type = st.sidebar.radio("Active Model", ["SMA Crossover", "RSI Momentum"])

if strategy_type == "SMA Crossover":
    st.sidebar.info("Moving Average Windows:")
    sma_fast = st.sidebar.slider("Fast MA Period", 5, 50, 20)
    sma_slow = st.sidebar.slider("Slow MA Period", 20, 200, 50)
else:
    st.sidebar.info("RSI Thresholds:")
    rsi_window = st.sidebar.slider("RSI Window", 5, 30, 14)
    rsi_low = st.sidebar.slider("Oversold (Buy)", 10, 40, 30)
    rsi_high = st.sidebar.slider("Overbought (Sell)", 60, 90, 70)

st.sidebar.markdown("---")
st.sidebar.write(f"**System Status:** Online")
st.sidebar.write(f"**Last Sync:** {datetime.now().strftime('%H:%M:%S')}")

st.title("Institutional Quantitative Analytics Platform")
st.caption("A Unified Framework for Univariate Analysis and Multi-Asset Portfolio Optimization")


tab1, tab2 = st.tabs(["Quant A: Single Asset", "Quant B: Portfolio Engine"])

with tab1:
    st.header("Quantitative Backtesting & ML Forecasting")
    
    selected_asset = st.selectbox(
        "Select Target Asset", 
        ["NVDA", "AAPL", "TSLA", "BTC-USD", "EURUSD=X", "GC=F"], 
        index=0
    )
    
    
    df = get_historical_data(selected_asset, horizon)
    
    if not df.empty:
    
        if strategy_type == "SMA Crossover":
            res = apply_sma_strategy(df, fast=sma_fast, slow=sma_slow)
        else:
            res = apply_rsi_strategy(df, window=rsi_window, low=rsi_low, high=rsi_high)
            
        
        sharpe, mdd = calculate_metrics(res['Returns'])
        

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Current Price", f"${df['Price'].iloc[-1]:,.2f}")
        col_m2.metric("Sharpe Ratio", sharpe)
        col_m3.metric("Max Drawdown", f"{mdd}%")
        col_m4.metric("Strategy Return", f"{(res['Cumulative'].iloc[-1]-1)*100:.1f}%")

        st.subheader("Performance Chart")
        fig_a = go.Figure()
        
        norm_price = df['Price'] / df['Price'].iloc[0]
        fig_a.add_trace(go.Scatter(x=df.index, y=norm_price, name="Asset (Raw)", line=dict(color='gray', width=1)))
        
        fig_a.add_trace(go.Scatter(x=res.index, y=res['Cumulative'], name="Strategy Value", line=dict(color='gold', width=3)))
        
        # ML Prediction (Bonus)
        preds = forecast_prices(df)
        future_dates = pd.date_range(df.index[-1], periods=6)[1:]
        fig_a.add_trace(go.Scatter(x=future_dates, y=preds/df['Price'].iloc[0], name="ML Forecast (5D)", line=dict(dash='dash', color='red')))
        
        fig_a.update_layout(template="plotly_dark", height=550)
        st.plotly_chart(fig_a, use_container_width=True)
    else:
        st.error("Connection error: Unable to retrieve data.")

with tab2:
    st.header("Portfolio Simulation & Risk Analytics")
    
    
    tickers = st.multiselect(
        "Select Portfolio Assets", 
        ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "AMZN", "BTC-USD", "GC=F"], 
        default=["AAPL", "NVDA", "BTC-USD"]
    )
    
    if len(tickers) >= 2:
        port_data = get_portfolio_data(tickers, horizon)
        
        if not port_data.empty:
            st.subheader("Portfolio Configuration")
            
            st.write("Allocation Weights:")
            weight_cols = st.columns(len(tickers))
            raw_weights = []
            for i, col in enumerate(weight_cols):
                w = col.number_input(f"{tickers[i]}", 0.0, 1.0, 1.0/len(tickers), 0.05, key=f"p_w_{tickers[i]}")
                raw_weights.append(w)
            
            weights = np.array(raw_weights)
            if weights.sum() != 1.0:
                weights = weights / weights.sum()
                st.caption(f"Normalized Weights: {np.round(weights, 2)}")

            
            results = calculate_portfolio_metrics(port_data, weights, rf_rate=rf_rate)
    
            km1, km2, km3 = st.columns(3)
            km1.metric("Portfolio Volatility (Ann.)", f"{results['volatility']*100:.2f}%")
            km2.metric("Portfolio Sharpe Ratio", results['sharpe'])
            km3.metric("Diversification Benefit", f"+{results['div_benefit']*100:.2f}%")

            st.subheader("Comparative Performance")
            fig_b = go.Figure()
            
            indiv_cum = results['individual_cum_returns']
            for ticker in tickers:
                fig_b.add_trace(go.Scatter(x=indiv_cum.index, y=indiv_cum[ticker], name=ticker, line=dict(width=1, dash='dot')))
            
            fig_b.add_trace(go.Scatter(x=results['cumulative'].index, y=results['cumulative'], name="TOTAL PORTFOLIO", line=dict(width=4, color='cyan')))
            
            fig_b.update_layout(template="plotly_dark", height=500, yaxis_title="Cumulative Growth")
            st.plotly_chart(fig_b, use_container_width=True)

            st.subheader("Correlation Analysis")
            fig_corr = px.imshow(results['correlation'], text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_corr.update_layout(template="plotly_dark")
            st.plotly_chart(fig_corr, use_container_width=True)
            
    else:
        st.warning("Please select at least 2 or 3 assets to start.")