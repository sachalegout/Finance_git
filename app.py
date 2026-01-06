import streamlit as st
import plotly.graph_objects as go
from src.quant_a.data_handler import get_historical_data, get_live_price
from src.quant_a.strategy_engine import (
    run_buy_and_hold_strategy, 
    run_ma_crossover_strategy, 
    calculate_performance_metrics
)

# Page configuration
st.set_page_config(page_title="Quant Analysis Platform", layout="wide")

st.title("📊 Quantitative Research Dashboard - NVIDIA")

# Sidebar for User Inputs
st.sidebar.header("Strategy Parameters")
ticker = "NVDA"
period = st.sidebar.selectbox("Select Period", ["6mo", "1y", "2y", "5y"], index=1)
strategy_type = st.sidebar.radio("Choose Strategy", ["Buy and Hold", "MA Crossover"])

# Specific parameters for MA Crossover
fast_ma = 20
slow_ma = 50
if strategy_type == "MA Crossover":
    fast_ma = st.sidebar.slider("Fast Moving Average", 5, 50, 20)
    slow_ma = st.sidebar.slider("Slow Moving Average", 51, 200, 50)

# Data Retrieval
data = get_historical_data(ticker, period)
live_price = get_live_price(ticker)

if not data.empty:
    # Header Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Current {ticker} Price", f"${live_price}")
    
    # Run selected strategy
    if strategy_type == "Buy and Hold":
        result_df = run_buy_and_hold_strategy(data)
    else:
        result_df = run_ma_crossover_strategy(data, fast_ma, slow_ma)
    
    # Performance Metrics
    sharpe, mdd = calculate_performance_metrics(result_df['Returns'])
    col2.metric("Sharpe Ratio", sharpe)
    col3.metric("Max Drawdown", f"{mdd*100}%")

    # Main Visualization (Two curves: Asset Price vs Strategy Value)
    st.subheader(f"Performance Analysis: {strategy_type}")
    
    fig = go.Figure()
    # Primary axis: Asset Price
    fig.add_trace(go.Scatter(x=result_df.index, y=result_df['Price'], name="NVDA Price", line=dict(color='royalblue')))
    # Secondary axis: Strategy Cumulative Return
    fig.add_trace(go.Scatter(x=result_df.index, y=result_df['Cumulative_Return'] * result_df['Price'].iloc[0], 
                             name="Strategy Value", line=dict(color='orange', dash='dot')))
    
    fig.update_layout(template="plotly_dark", hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Unable to load data. Please check your connection or Ticker.")