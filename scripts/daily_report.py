import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.quant_a.data_handler import get_historical_data
from src.quant_a.strategy_engine import calculate_metrics

def generate_daily_report():
    """
    Script to create a daily summary. 
    This will be scheduled on the AWS server (Cron job).
    """
    ticker = "NVDA"
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create the data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    report_path = f"data/report_{today}.txt"
    
    
    df = get_historical_data(ticker, period="1mo")
    
    if df.empty:
        print("Could not get data.")
        return

    returns = df['Price'].pct_change().dropna()
    sharpe, mdd = calculate_metrics(returns)
    

    report_text = f"""
=========================================
DAILY REPORT - {today}
=========================================
Asset: {ticker}
Current Price: ${df['Price'].iloc[-1]:.2f}
-----------------------------------------
Performance (1 Month):
- Sharpe Ratio: {sharpe}
- Max Drawdown: {mdd}%
-----------------------------------------
Status: Automated generation successful.
=========================================
"""
    with open(report_path, "w") as f:
        f.write(report_text)
    
    print(f"Report saved at {report_path}")

if __name__ == "__main__":
    generate_daily_report()