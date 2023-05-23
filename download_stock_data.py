import yfinance as yf
import os

# Define the tickers and date range
tickers = ['GOOGL', 'MSFT', 'AMZN', 'AAPL']
start_date = '2018-01-01'
end_date = '2022-12-31'

# Create directories to store the downloaded CSV files
os.makedirs('stock_data', exist_ok=True)

# Download the stock data with Open and Close prices, and quarterly earnings data
# Save as CSV files
for ticker in tickers:
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data[['Open', 'Close']]  # Keep only Open and Close columns
    stock_file_path = os.path.join('stock_data', f'{ticker}_2018_2022.csv')
    stock_data.to_csv(stock_file_path)
    print(f'{ticker} stock data saved to {stock_file_path}')


