import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
import talib as ta
import numpy as np
import mplfinance as mpf
from scipy.signal import argrelextrema

#user inputs, summary table(historical data), their indicators, and the plot


#user inputs from the user, pair/stock, start data and timeframe
def get_ticker_data(symbol, start_date, interval):
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    try:
        df = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=False
        )
        if df.empty:
            print(f"No data found for {symbol} between {start_date} and {end_date}.")
            return None
        return df

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

#plotting the data using close price
def plot_data(df, symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label=f'{symbol} Close Price')

    plt.title(f'{symbol} Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(False)
    plt.show()

#functions to calculate technical indicators(e.g., SMA, RSI, FIBONACCI)
def plot_ema(df, symbol, period):
    if df is None or df.empty or 'Close' not in df.columns:
        print("Data invalid or missing 'Close' column.")
        return

    #convert Close column to float NumPy 1D array
    close_prices = df['Close'].astype(float).to_numpy().ravel()
    # print("Close prices shape:", close_prices.shape)

    if close_prices.ndim != 1:
        print("Error: Close prices are not 1D.")
        return

    try:
        ema = ta.EMA(close_prices, timeperiod=period)
    except Exception as e:
        print("TA-Lib EMA calculation failed:", e)
        return

    df[f'EMA_{period}'] = ema

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue')
    plt.plot(df.index, df[f'EMA_{period}'], label=f'{period}-Day EMA', color='orange')
    plt.title(f"{symbol} - Close Price & {period}-Day EMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def plot_rsi(df, symbol, period):
    if df is None or df.empty or 'Close' not in df.columns:
        print("Data invalid or missing 'Close' column.")
        return

    #convert Close column to float NumPy 1D array
    close_prices = df['Close'].astype(float).to_numpy().ravel()
    # print("Close prices shape:", close_prices.shape)

    if close_prices.ndim != 1:
        print("Error: Close prices are not 1D.")
        return

    try:
        rsi = ta.RSI(close_prices, timeperiod=period)
    except Exception as e:
        print("TA-Lib RSI calculation failed:", e)
        return

    df['RSI'] = rsi

    plt.figure(figsize=(12, 5))
    plt.plot(df.index, rsi, label=f'RSI ({period})', color='orange')
    plt.axhline(70, linestyle='--', color='red', label='Overbought')
    plt.axhline(30, linestyle='--', color='green', label='Oversold')
    plt.title(f"{symbol} - RSI Indicator")
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def plot_fibonacci(ticker_data, symbol):
    if ticker_data is None or ticker_data.empty:
        print("No data to plot Fibonacci levels.")
        return

    high_price = ticker_data['High'].max()
    low_price = ticker_data['Low'].min()
    
    high_price = float(high_price)
    low_price = float(low_price)
    diff = high_price - low_price

    #fibonacci levels (standard retracement levels)
    levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    fib_levels = [high_price - (diff * level) for level in levels]

    plt.figure(figsize=(12, 6))
    plt.plot(ticker_data['Close'], label='Close Price', color='blue')
    for i, level in enumerate(fib_levels):
        plt.axhline(level, linestyle='--', label=f"{int(levels[i]*100)}% = {level:.2f}")

    plt.title(f"{symbol} - Fibonacci Retracement Levels")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="lower right")
    plt.grid(False)
    plt.tight_layout()
    plt.show()

#visualization of the data using candlesticks
def ensure_numeric(df, columns):
    df.columns = [col[0] for col in df.columns]
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=columns, inplace=True)
    return df

def plot_candlestick(df, symbol):
    if df is None or df.empty:
        print("No data to plot candlestick chart.")
        return
    
    df = ensure_numeric(df, ['Open', 'High', 'Low', 'Close'])
    mpf.plot(df, type='candle', style='yahoo', title=f"{symbol} Candlestick Chart", volume=False)

#implementing drawing tools like trend lines, support and resistance, supply and demand zones   
def auto_trendlines(df, symbol):
    df = df.copy()
    df.index.name = "Date"
    ensure_numeric(df, ['Open', 'High', 'Low', 'Close'])

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    local_min = argrelextrema(df['Low'].values, np.less_equal, order=5)[0]
    local_max = argrelextrema(df['High'].values, np.greater_equal, order=5)[0]

    x = np.arange(len(df))
    min_x = x[local_min]
    max_x = x[local_max]
    min_y = df['Low'].iloc[local_min].values.flatten()
    max_y = df['High'].iloc[local_max].values.flatten()

    support = np.poly1d(np.polyfit(min_x, min_y, 1)) if len(min_x) >= 2 else None
    resistance = np.poly1d(np.polyfit(max_x, max_y, 1)) if len(max_x) >= 2 else None

    x_vals = np.arange(len(df))
    trendlines = []

    if support:
        support_line = support(x_vals)
        trendlines.append(mpf.make_addplot(support_line, color='black'))
    
    if resistance:
        resistance_line = resistance(x_vals)
        trendlines.append(mpf.make_addplot(resistance_line, color='black'))

    mpf.plot(df, type='candle', style='yahoo', title=symbol,
             addplot=trendlines, ylabel='Price', volume=False, figratio=(16,9), figscale=1.2, tight_layout=True)

def plot_supply_demand_zones(df, symbol):
    df = df.copy()
    ensure_numeric(df, ['Open', 'High', 'Low', 'Close'])
    df.index.name = 'Date'
    df['range'] = df['High'] - df['Low']
    
    supply_zones = []
    demand_zones = []

    for i in range(2, len(df) - 3):
        cluster = df.iloc[i-2:i+1]
        avg_range = cluster['range'].mean()
        next_candle = df.iloc[i+1]
        breakout = next_candle['Close'] - next_candle['Open']
        
        if avg_range < 1.5 * df['range'].mean() and breakout > 1.5 * df['range'].mean():
            zone_low = cluster['Low'].min()
            zone_high = cluster['High'].max()
            demand_zones.append((df.index[i], zone_low, zone_high))

        elif avg_range < 1.5 * df['range'].mean() and breakout < -1.5 * df['range'].mean():
            zone_low = cluster['Low'].min()
            zone_high = cluster['High'].max()
            supply_zones.append((df.index[i], zone_low, zone_high))

    fig, ax = mpf.plot(df, type='candle', style='yahoo', returnfig=True, figsize=(14,8))

    for date, low, high in demand_zones:
        x_pos = mdates.date2num(date)
        ax[0].add_patch(patches.Rectangle((x_pos, low), width=5, height=high-low, color='green', alpha=0.2))
        ax[0].text(x_pos, high + (0.005 * high), 'Demand Zone', color='green', fontsize=9, weight='bold')

    for date, low, high in supply_zones:
        x_pos = mdates.date2num(date)
        ax[0].add_patch(patches.Rectangle((x_pos, low), width=5, height=high-low, color='red', alpha=0.2))
        ax[0].text(x_pos, high + (0.005 * high), 'Supply Zone', color='red', fontsize=9, weight='bold')

    plt.title(f"{symbol} with Auto Supply and Demand Zones")
    plt.tight_layout()
    plt.show()

#main program
if __name__ == "__main__":
    symbol = input("Enter the stock symbol (e.g., AAPL): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    interval = input("Enter the interval (e.g., 1d, 1wk, 1mo): ")

    ticker_data = get_ticker_data(symbol, start_date, interval)
    if ticker_data is not None:
        # print(ticker_data.head())
        # plot_data(ticker_data, symbol)
        # plot_ema(ticker_data, symbol, period=50)
        # plot_rsi(ticker_data, symbol, period=14)
        # plot_fibonacci(ticker_data, symbol)
        # plot_candlestick(ticker_data, symbol)
        # auto_trendlines(ticker_data, symbol)
        plot_supply_demand_zones(ticker_data, symbol)

    else:
        print("Failed to retrieve data.")