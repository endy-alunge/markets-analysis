#required libraries
import yfinance as yf
import pandas as pd
from pathlib import Path

# Define target folder and filename
target_dir = Path("C:/Users/Student/.vscode/Projects-2025/markets-analysis/historical_data")
target_dir.mkdir(parents=True, exist_ok=True)

#fetching data from yfinance(2023 - 2025 for now)
def fetch_yahoo_data(symbol, start="2025-01-01", end=None):
    data = yf.download(symbol, start=start, end=end)
    if data.empty:
        print(f"No data found for {symbol}.")
        return None
    
    #creating a txt file for a pair and save to historical data
    filename = target_dir / f"{symbol}_history.txt"
    data.to_csv(filename)
    print(f"Saved data to {filename}")
    return data

#we retrieve data of all available pairs, stock, etc
if __name__ == "__main__":

    symbols = [
    "EURUSD=X", "USDJPY=X", "GBPUSD=X", "USDCHF=X",
    "USDCAD=X", "AUDUSD=X", "NZDUSD=X", "USDZAR=X",
    "EURJPY=X", "GBPJPY=X",
    
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA",
    "NVDA", "META", "NFLX", "JPM", "BRK-B"
]
    
    print("Starting fetch for all pairs...\n")
    for symbol in symbols:
        fetch_yahoo_data(symbol)

    print("\n Done fetching all available pairs.")
