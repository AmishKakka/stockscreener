import pandas as pd
import datetime
import yfinance as source

# URLs for the NASDAQ Trader Symbol Directory files
nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
other_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"

# Load NASDAQ-listed stocks
nasdaq_columns = ["Symbol", "Name", "Market Category", "Test Issue", "Financial Status", "Round Lot Size"]
nasdaq_data = pd.read_csv(nasdaq_url, sep="|", names=nasdaq_columns)

# Remove the last row (footer info)
nasdaq_data = nasdaq_data[:-1]

# Load other-listed stocks (including NYSE, AMEX, etc.)
other_columns = ["Symbol", "Name", "Exchange", "CQS Symbol", "ETF", "Round Lot Size", "Test Issue", "NAICS Code"]
other_data = pd.read_csv(other_url, sep="|", names=other_columns)

# Filter for NYSE stocks
nyse_stocks = other_data[other_data["Exchange"] == "N"]

# Combine NYSE and NASDAQ tickers into one DataFrame
nyse_tickers = nyse_stocks[["Symbol", "Name"]]
nasdaq_tickers = nasdaq_data[["Symbol", "Name"]]
all_tickers = pd.concat([nyse_tickers, nasdaq_tickers])

# Display the total tickers
print(f"Total NYSE Stocks: {len(nyse_tickers)}")
print(f"Total NASDAQ Stocks: {len(nasdaq_tickers)}")
print(f"Total Combined Stocks: {len(all_tickers)}")

today = datetime.datetime.now().date().strftime("%Y-%m-%d")
count = 0
for t in list(all_tickers["Symbol"]):
    data  = source.download(t, start=today) 
    print(data.columns)
    count += 1
print("Found in total: ", count)