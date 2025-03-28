import yfinance as yf
from datetime import datetime, timedelta

def get_last_week_prices(ticker):
    # Calculate the date range for the last week
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch historical data
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        print(f"No data found for ticker {ticker} in the last week.")
        return

    price_str = ""

    for date, row in hist.iterrows():
        price_str += f"Date: {date.strftime('%Y-%m-%d')}, Open: {row['Open']:.2f}, Close: {row['Close']:.2f} \n"
    
    return price_str


