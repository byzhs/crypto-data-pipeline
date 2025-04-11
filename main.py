import pandas as pd
import requests
import matplotlib.pyplot as plt
import logging

# log file
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Pipeline started.")

# Load historical data
try:
    historical_df = pd.read_csv('historical_prices.csv')
    historical_df.rename(columns={'snapped_at': 'Date', 'price': 'Price USD'}, inplace=True)
    if 'Coin' not in historical_df.columns:
        historical_df['Coin'] = 'bitcoin'
    logging.info("Historical CSV loaded.")
except Exception as e:
    logging.error(f"Error loading historical data: {e}")
    raise

# Fetch live data
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana"
}

try:
    response = requests.get(url, params=params).json()
    live_df = pd.DataFrame(response)[['id', 'current_price', 'market_cap', 'total_volume']]
    live_df.columns = ['Coin', 'Current Price (USD)', 'Market Cap', '24h Volume']
    logging.info("Live prices fetched from API.")
except Exception as e:
    logging.error(f"Error fetching live prices: {e}")
    raise

# Merge and calculate change
try:
    latest_hist_df = historical_df[historical_df['Date'] == historical_df['Date'].max()]
    merged_df = pd.merge(latest_hist_df, live_df, on='Coin', how='inner')
    merged_df['Price Change (%)'] = ((merged_df['Current Price (USD)'] - merged_df['Price USD']) / merged_df['Price USD']) * 100
except Exception as e:
    logging.error(f"Error during merging or processing: {e}")
    raise

# Save report to Excel
try:
    with pd.ExcelWriter("crypto_report.xlsx", engine="openpyxl") as writer:
        historical_df.to_excel(writer, sheet_name="Historical Data", index=False)
        live_df.to_excel(writer, sheet_name="Live Prices", index=False)
        merged_df.to_excel(writer, sheet_name="Comparison", index=False)
    logging.info("Excel report generated.")
except Exception as e:
    logging.error(f"Error saving Excel report: {e}")
    raise

# Prepare data for plotting
try:
    btc_history = historical_df[historical_df['Coin'] == 'bitcoin'].copy()
    btc_history['Date'] = pd.to_datetime(btc_history['Date'])
    btc_history.sort_values(by='Date', inplace=True)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(btc_history['Date'], btc_history['Price USD'], marker='o', linestyle='-')
    plt.title("Bitcoin Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price USD")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("bitcoin_price_chart.png")
    plt.show()
    logging.info("Bitcoin chart saved.")
except Exception as e:
    logging.error(f"Error saving chart: {e}")


########

try:
    # Bar chart: Price change comparison
    plt.figure(figsize=(7, 5))
    plt.bar(merged_df['Coin'], merged_df['Price Change (%)'], color='skyblue')
    plt.title("Price Change (%) - Latest vs. Historical")
    plt.ylabel("Percent Change")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("price_change_comparison.png")
    plt.show()
    logging.info("Comparison chart saved.")
except Exception as e:
    logging.error(f"Error saving comparison chart: {e}")
