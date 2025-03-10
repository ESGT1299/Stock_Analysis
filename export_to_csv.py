import pandas as pd
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

# ✅ Export Data to CSV for Tableau
csv_filename = "Bitcoin_stock_analysis.csv"
stock_data.to_csv(csv_filename, index=False)

print(f"✅ Data exported successfully to {csv_filename}!")

