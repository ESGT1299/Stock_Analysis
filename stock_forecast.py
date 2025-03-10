import pandas as pd
from sqlalchemy import create_engine
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# ✅ Connect to PostgreSQL
db_username = "postgres"
db_password = "ESgt09601698."
db_host = "localhost"
db_port = "5432"
db_name = "finance_db"

engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

# ✅ Query stock data
query = """
SELECT date, close_price
FROM stock_data
WHERE symbol = 'BTC-USD'
ORDER BY date ASC;
"""

stock_data = pd.read_sql(query, engine)
stock_data["date"] = pd.to_datetime(stock_data["date"])
stock_data.set_index("date", inplace=True)

# ✅ Train ARIMA Model
model = ARIMA(stock_data["close_price"], order=(5,1,0))  # (p,d,q) = (5,1,0)
model_fit = model.fit()

# ✅ Forecast Next 30 Days
forecast = model_fit.forecast(steps=30)
future_dates = pd.date_range(start=stock_data.index[-1], periods=30, freq="D")

# ✅ Plot Predictions
plt.figure(figsize=(12, 6))
plt.plot(stock_data.index, stock_data["close_price"], label="Historical Prices", color="blue")
plt.plot(future_dates, forecast, label="Predicted Prices", color="red", linestyle="dashed")
plt.title("Stock Price Prediction using ARIMA")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid()
plt.show()
