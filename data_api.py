#required libraries
import yfinance as yf
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

#define target folder and filename
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

# Required libraries
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import talib as ta

# Define target folder
target_dir = Path("C:/Users/Student/.vscode/Projects-2025/markets-analysis/historical_data")
target_dir.mkdir(parents=True, exist_ok=True)

# Fetching data with user-defined start, end, interval
def fetch_yahoo_data(symbol, start="2023-01-01", end=None, interval="1d"):
    if end is None or end.strip() == "":
        end = datetime.today().strftime('%Y-%m-%d')

    print(f" Fetching {symbol} from {start} to {end} | interval: {interval}")

    try:
        data = yf.download(
            symbol,
            start=start,
            end=end,
            interval=interval,
            progress=False
        )

        if data.empty:
            print(f" No data found for {symbol} in that range.")
            return None

        #save to file
        filename = target_dir / f"{symbol}_history.txt"
        data.to_csv(filename)
        print(f"Saved to {filename}")
        return data

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

#we retrieve data of all available pairs, stock, etc
if __name__ == "__main__":

    symbols = [
    "USDCAD=X", "AUDUSD=X", "NZDUSD=X", "USDZAR=X",
    
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA",
]
    
    print("Starting fetch for all pairs...\n")
    for symbol in symbols:
        fetch_yahoo_data(symbol)

    print("\n Done fetching all available pairs.")