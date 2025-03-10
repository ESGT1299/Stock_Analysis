import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ✅ Connect to PostgreSQL
db_username = "postgres"
db_password = "ESgt09601698."  # Replace with your actual PostgreSQL password
db_host = "localhost"
db_port = "5432"
db_name = "finance_db"

engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

# ✅ Query stock data
query = """
SELECT date, close_price, volume
FROM stock_data
WHERE symbol = 'BTC-USD'
ORDER BY date ASC;
"""

stock_data = pd.read_sql(query, engine)
stock_data["date"] = pd.to_datetime(stock_data["date"])

# ✅ Moving Averages (50-day & 200-day)
stock_data["MA_50"] = stock_data["close_price"].rolling(window=50).mean()
stock_data["MA_200"] = stock_data["close_price"].rolling(window=200).mean()

# ✅ Bollinger Bands (20-day)
stock_data["BB_Middle"] = stock_data["close_price"].rolling(window=20).mean()
stock_data["BB_Upper"] = stock_data["BB_Middle"] + 2 * stock_data["close_price"].rolling(window=20).std()
stock_data["BB_Lower"] = stock_data["BB_Middle"] - 2 * stock_data["close_price"].rolling(window=20).std()

# ✅ Average True Range (ATR)
stock_data["High-Low"] = stock_data["close_price"].rolling(window=14).max() - stock_data["close_price"].rolling(window=14).min()
stock_data["ATR"] = stock_data["High-Low"].rolling(window=14).mean()

# ✅ Plotting with Matplotlib & Seaborn
plt.figure(figsize=(14, 6))
sns.lineplot(data=stock_data, x="date", y="close_price", label="Closing Price", color="blue")
sns.lineplot(data=stock_data, x="date", y="MA_50", label="50-Day MA", color="red", linestyle="dashed")
sns.lineplot(data=stock_data, x="date", y="MA_200", label="200-Day MA", color="green", linestyle="dashed")
plt.fill_between(stock_data["date"], stock_data["BB_Lower"], stock_data["BB_Upper"], color='gray', alpha=0.2, label="Bollinger Bands")
plt.title("Stock Price with Moving Averages & Bollinger Bands")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid()
plt.show()

