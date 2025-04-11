# 📈 Crypto Data Pipeline Project

This project automates the extraction and analysis of cryptocurrency price data using Python. It merges historical prices with real-time data from the CoinGecko API and generates an Excel report and charts.

---

## 🔧 Technologies Used
- Python
- pandas
- requests
- matplotlib
- openpyxl
- logging

---

## 📌 What It Does
- Loads historical crypto price data from a local CSV file
- Fetches live market data from CoinGecko's free public API
- Merges and compares the two datasets
- Calculates price change percentages
- Generates:
  - A multi-sheet Excel report
  - A line chart of Bitcoin price history
  - A bar chart comparing recent price changes

---

## 📁 Output Files
- `crypto_report.xlsx` — includes Historical Data, Live Prices, and Comparison
- `bitcoin_price_chart.png` — Bitcoin price over time
- `price_change_comparison.png` — Latest % change across Bitcoin, Ethereum, and Solana
- `pipeline.log` — timestamped logging of all steps

---

## 🧪 Example Historical File Format (`historical_prices.csv`)
```csv
snapped_at,price,market_cap,total_volume
2024-04-01 00:00:00 UTC,67890,1400000000000,100000000
2024-04-02 00:00:00 UTC,68250,1420000000000,110000000
...
