# Stock Price Tracker and News Report Generator



This system consists of two main components:
1. **Stock Price Tracker**: A Python script that tracks the price of a stock in real-time and sends desktop notifications when significant price changes occur.
2. **Streamlit News Report Generator**: A Streamlit-based web application that searches for recent news about a stock and generates a detailed report using AI.

![streamlit News Report Generator](img/Screenshot%202025-03-28%20at%2011.40.09 PM.jpg)

---

## 1. Stock Price Tracker

### Description
The Stock Price Tracker monitors the price of a specified stock in real-time. It sends desktop notifications when the price changes by a specified percentage threshold.

### Features
- Fetches real-time stock prices using the `yfinance` library.
- Sends desktop notifications for significant price changes.
- Configurable threshold percentage and check interval.

### How to Use
1. Navigate to the `src` directory.
2. Run the `price_tracking.py` script:
   ```bash
   python price_tracking.py
   ```
3. Modify the following parameters in the script as needed:
   - `STOCK_SYMBOL`: The stock ticker symbol (e.g., `AAPL` for Apple).
   - `THRESHOLD`: The percentage change to trigger notifications.
   - `INTERVAL`: The time interval (in seconds) between price checks.

---

## 2. Streamlit News Report Generator

### Description
The Streamlit app allows users to input a stock ticker symbol and generates a detailed report summarizing recent news about the stock. The report is created using AI and includes citations for the news sources.

### Features
- Fetches recent news articles about the stock.
- Summarizes news and includes relevant price information.
- Generates a structured report with proper citations.

### How to Use
1. Navigate to the `src` directory.
2. Run the Streamlit app:
   ```bash
   streamlit run streamlit.py
   ```
3. Open the app in your browser (Streamlit will provide a local URL).
4. Enter a stock ticker symbol (e.g., `AAPL`, `TSLA`) in the input field.
5. Click the "Generate Report" button to view the report and citations.

---

## Requirements

### Python Libraries
- `streamlit`
- `yfinance`
- `plyer`
- `openai`
- `pandas`

### API Keys
- **OpenAI API Key**: Required for generating AI-based reports.
- **NewsAPI Key**: Required for fetching news articles.

Add your API keys to the `Config` class in `report_generate.py`.

---

## Notes
- Ensure you have a stable internet connection for real-time price tracking and news fetching.
- The system is designed for educational purposes and may require further customization for production use.
