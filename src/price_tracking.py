import yfinance as yf
import time
from plyer import notification
from datetime import datetime

def get_stock_price(ticker_symbol):
    """Get current stock price using yfinance"""
    stock = yf.Ticker(ticker_symbol)
    return stock.info['regularMarketPrice']

def send_notification(title, message):
    """Send desktop notification"""
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10,
    )

def track_stock_price(ticker_symbol, threshold_percent=2.0, check_interval=300):
    """
    Track stock price and notify on significant changes
    Args:
        ticker_symbol: Stock symbol (e.g., 'AAPL')
        threshold_percent: Percentage change to trigger notification
        check_interval: Time between checks in seconds (default 5 minutes)
    """
    print(f"Starting to track {ticker_symbol}...")
    
    # Get initial price
    initial_price = get_stock_price(ticker_symbol)
    last_price = initial_price
    
    while True:
        try:
            current_price = get_stock_price(ticker_symbol)
            price_change = ((current_price - last_price) / last_price) * 100
            
            # Check if price change exceeds threshold
            if abs(price_change) >= threshold_percent:
                message = (f"Price changed by {price_change:.2f}%\n"
                         f"From: ${last_price:.2f}\n"
                         f"To: ${current_price:.2f}")
                
                send_notification(
                    f"{ticker_symbol} Price Alert!",
                    message
                )
                last_price = current_price
            
            # Print current status
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] {ticker_symbol}: ${current_price:.2f}")
            
            time.sleep(check_interval)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(check_interval)

if __name__ == "__main__":
    # Example usage
    STOCK_SYMBOL = "AAPL"  # Change this to your desired stock
    THRESHOLD = 2.0        # Notification threshold (percentage)
    INTERVAL = 30        # Check every 30 seconds
    
    track_stock_price(STOCK_SYMBOL, THRESHOLD, INTERVAL)