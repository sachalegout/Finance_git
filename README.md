# Finance Project - Institutional Terminal 

This is a Python project for our finance class. We built a dashboard to analyze stocks and manage portfolios using Streamlit.

## What it does

### Part A: Stock Analysis
- **Strategies**: We use SMA Crossover and RSI to find buy/sell signals.
- **Metrics**: The app calculates the Sharpe Ratio and Max Drawdown.
- **AI Bonus**: We added a Linear Regression model to predict prices for the next 5 days.

### Part B: Portfolio Management
- **Multi-asset**: You can pick 3 or more stocks (like AAPL, NVDA, TSLA).
- **Weights**: You can choose how much % to put in each stock.
- **Risk**: The app shows the correlation matrix and how much risk is reduced by diversification.

### Automation
- **Daily Report**: A script runs on the server every day to save market data in a text file.

## How to use it
1. Install everything: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`