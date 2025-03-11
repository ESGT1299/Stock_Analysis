# 📊 Stock Price Analysis: EMA, MACD, RSI & Trading Volume with ARIMA Forecasting

## 📝 Project Overview
This project provides **a complete financial analysis** of **Bitcoin (BTC-USD)**, leveraging **technical indicators** to study price movements and **ARIMA forecasting** for predicting future trends. The analysis is divided into two key sections:

1️⃣ **Historical Data Analysis** using **Exponential Moving Averages (EMA), Moving Average Convergence Divergence (MACD), Relative Strength Index (RSI), and Trading Volume** to evaluate past price movements.

2️⃣ **Stock Price Forecasting** using an **optimized ARIMA model**, predicting **Bitcoin’s price for the next 30 days**.

The **historical data is sourced from a dedicated ETL Pipeline project**, ensuring **data consistency and quality** before analysis. While **technical analysis is visualized in Tableau**, **forecasting is conducted and plotted exclusively in Python**, providing accurate projections based on time-series modeling.

---

## 🎯 Key Objectives
- ✅ **Analyze Bitcoin price trends** with **technical indicators**.
- ✅ **Predict future prices** using **time-series forecasting**.
- ✅ **Visualize historical data trends** in **Tableau**.
- ✅ **Support traders and analysts** in making **data-driven decisions**.

---

## ⚡ Why This Project Matters
Financial markets are inherently **volatile**, requiring **data-driven insights** for decision-making. By combining **technical indicators and time-series forecasting**, this project enables **better market understanding and risk management**.

- **Trend Analysis:** EMA helps identify **short-term & long-term price directions**.
- **Momentum Measurement:** MACD detects **bullish or bearish strength**.
- **Market Condition Assessment:** RSI signals **overbought or oversold conditions**.
- **Price Forecasting:** ARIMA predicts **short-term price movements** based on historical data.

Using these tools, traders can make **more informed investment decisions**, reducing uncertainty and improving profitability.

---

## 🛠️ Technologies Used
- **Python** – Data analysis & forecasting.
- **Pandas & NumPy** – Data manipulation & statistical calculations.
- **Matplotlib & Seaborn** – Data visualization.
- **Statsmodels (ARIMA)** – Time-series forecasting.
- **PostgreSQL (SQLAlchemy)** – Data storage & retrieval.
- **Tableau** – Interactive **historical data visualization**.
- **Git & GitHub** – Version control & project tracking.

---

## 📊 **Tableau Dashboard (Historical Data)**
### 🔹 **Dashboard Components**
The **Tableau dashboard** presents **historical Bitcoin price movements** through **technical indicators**, helping analysts understand past market behavior.

1️⃣ **Bitcoin Price with 12-Day & 26-Day EMA**  
   - **Why EMA?** Exponential Moving Average gives **higher weight to recent prices**, reacting **faster** to market movements than a **Simple Moving Average (SMA)**.
   - **How it works:** The **12-day EMA (short-term)** and **26-day EMA (long-term)** help detect trend shifts.
   - **Buy Signal:** 12-day EMA crossing **above** 26-day EMA.
   - **Sell Signal:** 12-day EMA crossing **below** 26-day EMA.

2️⃣ **MACD Indicator: Histogram, MACD Line & Signal Line**  
   - **Why MACD?** Measures **momentum** and **trend direction**.
   - **How it works:** MACD = (12-day EMA - 26-day EMA).  
   - The **Signal Line (9-day EMA of MACD)** is used for crossovers:
     - **Bullish crossover:** MACD **rises above** Signal Line → **Buy**.
     - **Bearish crossover:** MACD **falls below** Signal Line → **Sell**.

3️⃣ **Relative Strength Index (RSI)**  
   - **Why RSI?** Measures **market momentum** to identify **overbought or oversold conditions**.
   - **How it works:** RSI ranges **from 0 to 100**:
     - **RSI > 70** = **Overbought** (possible price drop).
     - **RSI < 30** = **Oversold** (possible price increase).

4️⃣ **Trading Volume Over Time**  
   - **Why Trading Volume?** Confirms the **strength of price movements**.
   - **How it works:** Large price swings **with high volume** indicate **strong trends**, while **low volume** suggests **false breakouts**.

🔗 **[View Interactive Tableau Dashboard](https://public.tableau.com/views/TableauDashboard_17416361239740/Dashboard1?:language=es-ES&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

---

## 📈 **Stock Price Forecasting (Python Only)**
### 🔹 **Why ARIMA?**
- ARIMA (**AutoRegressive Integrated Moving Average**) is a **statistical model** that captures **trends, seasonality, and patterns** in time-series data.
- Unlike basic moving averages, ARIMA uses **past values** to make accurate predictions.

### 🔹 **How the ARIMA Model Works**
1️⃣ **Checks Data Stationarity**  
   - ARIMA requires **stationary data** (constant mean & variance over time).  
   - The **Augmented Dickey-Fuller (ADF) Test** determines if differencing is required.

2️⃣ **Parameter Selection (p, d, q)**  
   - **p (AutoRegression - AR):** Past values used in prediction.  
   - **d (Differencing - I):** How many times to make data stationary.  
   - **q (Moving Average - MA):** Past errors included in the model.

3️⃣ **Grid Search Optimization**  
   - The best **(p, d, q)** parameters are selected **automatically** using **AIC (Akaike Information Criterion)**.

4️⃣ **Forecasting the Next 30 Days**  
   - The trained ARIMA model **predicts Bitcoin prices** for the next **30 days**.
   - The results include a **confidence interval** to show potential volatility.

5️⃣ **Visualization (Python Plot Only)**  
   - Historical prices are plotted in **blue**.
   - Forecasted prices are shown in **red dashed lines**.
   - Confidence intervals appear as **shaded pink areas**.

📌 **ARIMA forecasting is NOT visualized in Tableau** because **Python offers more accurate and professional forecasting tools**.

---

## 📂 **Project Structure**
```
📂 FINANCE_PROJECT
│── 📂 ETL_Pipeline  # Data cleaning & preparation scripts
│── 📂 Stock_Analysis
│   │── stock_analysis.py  # Technical indicators analysis
│   │── stock_forecast.py  # ARIMA-based forecasting
│   │── export_to_csv.py  # Exports clean data for Tableau
│   │── Bitcoin_stock_analysis.csv  # Historical stock data
│   │── Bitcoin_stock_analysis_updated.csv  # Historical + Forecasted data
│── 📂 Tableau_Dashboard.twb  # Tableau visualization workbook
│── README.md  # Project Documentation
```

---

## 🛠️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ESGT1299/Stock_Analysis.git
cd Stock_Analysis
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Analysis
```bash
python stock_analysis.py
python export_to_csv.py
python stock_forecast.py
```
### 4️⃣ Load Data into Tableau
Open Tableau and import the data obtained from the **export_to_csv.py** file.


## 📢 Conclusion
This project successfully integrates technical analysis with forecasting to provide data-driven market insights. By leveraging Python for analysis and Tableau for visualization, we create a powerful tool for traders & analysts.

**🚀 Future Work**: Implement LSTM deep learning models for improved forecasting accuracy.

## 📌 Key Takeaways
✔️ **Technical indicators provide actionable insights** into stock market trends.

✔️ **ARIMA modeling enhances decision-making** with short-term price predictions.

✔️ **Tableau dashboards enable effective communication** of financial trends.

✔️ **Combining multiple analysis techniques improves forecasting accuracy**.

---

## 🤝 Contribution & Contact
This project is part of my **financial data science portfolio**, demonstrating expertise in **quantitative analysis, machine learning, and data visualization**. 

For feedback, collaboration, or inquiries, feel free to reach out!

📧 **Contact:** [Linkedin](https://www.linkedin.com/in/erick-guagua-14b143214/)
