import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the tickers
tickers = ['GOOGL', 'MSFT', 'AMZN', 'AAPL']

# Initialize an empty DataFrame to store the stock data
stock_data = pd.DataFrame()

# Read the stock data CSV files
for ticker in tickers:
    stock_file_path = os.path.join('stock_data', f'{ticker}_2018_2022.csv')
    data = pd.read_csv(stock_file_path, index_col='Date', parse_dates=True)
    stock_data[ticker] = data['Close']

# Calculate the moving averages for each stock
sma_20 = stock_data.rolling(window=20).mean()
sma_50 = stock_data.rolling(window=50).mean()

# Plot the stock prices and moving averages
plt.figure(figsize=(14, 8))
for ticker in tickers:
    plt.plot(stock_data[ticker], label=ticker)
    plt.plot(sma_20[ticker], label=ticker+'_SMA20')
    plt.plot(sma_50[ticker], label=ticker+'_SMA50')
plt.title('Closing Stock Prices (2018-2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Resample the data to yearly frequency and calculate the percentage change for each year
pct_change = stock_data.resample('Y').last().pct_change()



# Calculate the percentage increase for each stock over the four years
pct_change = (stock_data.iloc[-1] - stock_data.iloc[0]) / stock_data.iloc[0] * 100

# Plot the percentage increase for each stock on a bar plot
plt.figure(figsize=(14, 8))
plt.bar(pct_change.index, pct_change, width=0.4)
plt.title('Percentage Increase in Stock Prices (2018-2022)')
plt.xlabel('Stock Ticker')
plt.ylabel('Percentage Increase')
plt.ylim([0, 200])
plt.show()