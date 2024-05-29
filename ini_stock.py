# download_stocks.py

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

def download_stock_data(tickers, start_date, end_date):
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        filename = f"{ticker}.csv"
        stock_data.to_csv(filename)
        print(f"Data for {ticker} has been saved to {filename}")

if __name__ == "__main__":
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    download_stock_data(tickers, start_date, end_date)
