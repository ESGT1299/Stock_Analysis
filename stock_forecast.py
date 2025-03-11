# import pandas as pd
# from sqlalchemy import create_engine
# from statsmodels.tsa.arima.model import ARIMA
# import matplotlib.pyplot as plt

# # ✅ Connect to PostgreSQL
# db_username = "postgres"
# db_password = "ESgt09601698."
# db_host = "localhost"
# db_port = "5432"
# db_name = "finance_db"

# engine = create_engine(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")

# # ✅ Query stock data
# query = """
# SELECT date, close_price
# FROM stock_data
# WHERE symbol = 'BTC-USD'
# ORDER BY date ASC;
# """

# stock_data = pd.read_sql(query, engine)
# stock_data["date"] = pd.to_datetime(stock_data["date"])
# stock_data.set_index("date", inplace=True)

# # ✅ Train ARIMA Model
# model = ARIMA(stock_data["close_price"], order=(5,1,0))  # (p,d,q) = (5,1,0)
# model_fit = model.fit()

# # ✅ Forecast Next 30 Days
# forecast = model_fit.forecast(steps=30)
# future_dates = pd.date_range(start=stock_data.index[-1], periods=30, freq="D")

# # ✅ Plot Predictions
# plt.figure(figsize=(12, 6))
# plt.plot(stock_data.index, stock_data["close_price"], label="Historical Prices", color="blue")
# plt.plot(future_dates, forecast, label="Predicted Prices", color="red", linestyle="dashed")
# plt.title("Stock Price Prediction using ARIMA")
# plt.xlabel("Date")
# plt.ylabel("Price ($)")
# plt.legend()
# plt.grid()
# plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import itertools
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sqlalchemy import create_engine

# ✅ Connect to PostgreSQL
db_username = "postgres"
db_password = "ESgt09601698."  # Replace with actual password
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

# ✅ Check for Stationarity (ADF Test)
adf_result = adfuller(stock_data["close_price"])
is_stationary = adf_result[1] < 0.05  # If p-value < 0.05, data is stationary

if not is_stationary:
    print("Data is NOT stationary. Applying differencing...")
    stock_data["diff_close_price"] = stock_data["close_price"].diff().dropna()
    use_diff = True
else:
    stock_data["diff_close_price"] = stock_data["close_price"]
    use_diff = False

# ✅ Grid Search for Best ARIMA (p, d, q)
p_values = range(0, 6)
d_values = range(0, 2)
q_values = range(0, 6)
best_aic = np.inf
best_order = None

for p, d, q in itertools.product(p_values, d_values, q_values):
    try:
        model = ARIMA(stock_data["diff_close_price"].dropna(), order=(p, d, q))
        results = model.fit()
        if results.aic < best_aic:
            best_aic = results.aic
            best_order = (p, d, q)
    except:
        continue

print(f"Best ARIMA Order: {best_order}")

# ✅ Train Best ARIMA Model
model = ARIMA(stock_data["diff_close_price"].dropna(), order=best_order)
model_fit = model.fit()

# ✅ Forecast Next 30 Days
forecast_steps = 30
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=stock_data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq="D")
forecast_values = forecast.predicted_mean
conf_int = forecast.conf_int()

# ✅ If differencing was applied, invert it to restore original price scale
if use_diff:
    last_actual_value = stock_data["close_price"].iloc[-1]
    forecast_values = last_actual_value + forecast_values.cumsum()
    conf_int.iloc[:, 0] = last_actual_value + conf_int.iloc[:, 0].cumsum()
    conf_int.iloc[:, 1] = last_actual_value + conf_int.iloc[:, 1].cumsum()

# ✅ Create a New DataFrame for Predictions
forecast_df = pd.DataFrame({
    "date": forecast_index,
    "close_price": forecast_values
})

# ✅ Combine Historical Data with Predictions
full_data = pd.concat([stock_data.reset_index()[["date", "close_price"]], forecast_df])

# ✅ Save Combined Data to CSV for Tableau
full_data.to_csv("Bitcoin_stock_analysis_updated.csv", index=False)
print("✅ Data saved successfully as 'Bitcoin_stock_analysis_updated.csv'")

# ✅ Plot Improved Predictions
plt.figure(figsize=(12, 6))
plt.plot(stock_data.index, stock_data["close_price"], label="Historical Prices", color="blue")
plt.plot(forecast_index, forecast_values, label="Predicted Prices", color="red", linestyle="dashed")
plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color="pink", alpha=0.3, label="Confidence Interval")
plt.axvline(x=stock_data.index[-1], color='black', linestyle="dotted", label="Forecast Start")
plt.title("Stock Price Prediction using Optimized ARIMA")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid()
plt.show()

