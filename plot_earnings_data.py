import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def cleanup_earnings_df(df):
    df.index=pd.to_datetime(df.index, format='%m/%d/%y')
    df['year'] = df.index.year
    df = df.set_index('year')
    df["Revenue"]=df["Revenue"].str.strip("$").str.strip().str.replace(',', '')
    df["Revenue"]=df["Revenue"].astype("float")

    df["Net Income"] = df["Net Income"].str.strip("$").str.strip().str.replace(',', '')
    df["Net Income"] = df["Net Income"].astype("float")

    df["Gross Profit"] = df["Gross Profit"].str.strip("$").str.strip().str.replace(',', '')
    df["Gross Profit"] = df["Gross Profit"].astype("float")
    df=df.sort_values(by=['year'])
    return df

# Read in the CSV files and create separate dataframes for each company
googl_df = pd.read_csv('earnings_data/GOOGL_earnings.csv', index_col='Date')
amzn_df = pd.read_csv('earnings_data/AMZN_earnings.csv', index_col='Date')
msft_df = pd.read_csv('earnings_data/MSFT_earnings.csv',index_col='Date')
aapl_df = pd.read_csv('earnings_data/AAPL_earnings.csv', index_col='Date')


googl_df=cleanup_earnings_df(googl_df)
amzn_df=cleanup_earnings_df(amzn_df)
msft_df=cleanup_earnings_df(msft_df)
aapl_df=cleanup_earnings_df(aapl_df)



# Create a new figure and axis object
fig, ax = plt.subplots()

# Plot the revenue trends for each DataFrame on the same plot
ax.plot(googl_df.index, googl_df['Revenue'], label='GOOGL')
ax.plot(aapl_df.index, aapl_df['Revenue'], label='AAPL')
ax.plot(msft_df.index, msft_df['Revenue'], label='MSFT')
ax.plot(amzn_df.index, amzn_df['Revenue'], label='AMZN')

# Add gridlines to the plot
ax.grid(True)

# Add a title and labels for the x- and y-axes
ax.set_title('Revenue Trends')
ax.set_xlabel('Year')
ax.set_ylabel('Revenue (Millions of US $)')

# Add a legend to identify each DataFrame
ax.legend()

# Display the plot
plt.show()

# Combine the net income columns for all DataFrames into one list
net_incomes = [googl_df['Net Income'], aapl_df['Net Income'], msft_df['Net Income'], amzn_df['Net Income']]


# Create a new figure and axis object
fig, ax = plt.subplots()

# Create an array of x-values for the bar plot
x_values = np.arange(len(net_incomes[0].index))

# Set the width of each bar
bar_width = 0.2

# Plot a bar for each DataFrame's net income values
ax.bar(x_values, net_incomes[0], width=bar_width, label='GOOGL')
ax.bar(x_values + bar_width, net_incomes[1], width=bar_width, label='AAPL')
ax.bar(x_values + 2 * bar_width, net_incomes[2], width=bar_width, label='MSFT')
ax.bar(x_values + 3 * bar_width, net_incomes[3], width=bar_width, label='AMZN')

# Add a title and labels for the x- and y-axis
ax.set_title('Net Income Trends')
ax.set_xlabel('Year')
ax.set_ylabel('Net Income (Millions of US $)')

# Add ticker labels for the x-axis
ax.set_xticks(x_values + 1.5 * bar_width)
ax.set_xticklabels(net_incomes[0].index)

# Add a legend to identify each DataFrame in the plot
ax.legend()

# Display the plot
plt.show()

# Set the figure size
fig, ax = plt.subplots(figsize=(12, 8))

# Define the bar width
bar_width = 0.2

# Set the x values for the bars
x_values = [2018,2019,2020,2021,2022]
x_values=np.asarray(x_values)
# Plot the gross profits for each company
ax.bar(x_values - 1.5*bar_width, googl_df['Gross Profit'], width=bar_width, label='GOOGL', color='blue')
ax.bar(x_values - 0.5*bar_width, aapl_df['Gross Profit'], width=bar_width, label='AAPL', color='orange')
ax.bar(x_values + 0.5*bar_width, msft_df['Gross Profit'], width=bar_width, label='MSFT', color='green')
ax.bar(x_values + 1.5*bar_width, amzn_df['Gross Profit'], width=bar_width, label='AMZN', color='red')

print(amzn_df["Gross Profit"])

# Set the title and axis labels
ax.set_title('Gross Profit Trends by Year')
ax.set_xlabel('Year')
ax.set_ylabel('Gross Profit (in millions)')

# Set the x-axis ticks and tick labels
ax.set_xticks(x_values)
ax.set_xticklabels(x_values)

# Add a legend
ax.legend()

# Display the plot
plt.show()











