import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import os

def get_news_from_newsapi(ticker, api_key, days_back=7, language='en'):
    """
    Fetch news for a stock ticker using NewsAPI
    Requires free API key from https://newsapi.org/
    """
    url = 'https://newsapi.org/v2/everything'
    
    # Calculate date range (today - days_back)
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    params = {
        'q': ticker,
        'from': from_date,
        'to': to_date,
        'language': language,
        'sortBy': 'publishedAt',
        'apiKey': api_key,
        'pageSize': 100  # Max allowed for free tier
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'ok' and data['totalResults'] > 0:
            articles = data['articles']
            # Create DataFrame with relevant fields
            news_df = pd.DataFrame(articles)[['source', 'author', 'title', 'description', 'url', 'publishedAt']]
            news_df['publishedAt'] = pd.to_datetime(news_df['publishedAt'])
            news_df['ticker'] = ticker
            # news_df = news_df.loc[news_df['author'] == 'finance.yahoo.com']
            return news_df
        else:
            print(f"No news found for {ticker} via NewsAPI")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error fetching news for {ticker} from NewsAPI: {e}")
        return pd.DataFrame()

def get_news_from_yfinance(ticker):
    """
    Fetch news for a stock ticker using Yahoo Finance as fallback
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        if news:
            news_df = pd.DataFrame(news)
            news_df = pd.DataFrame(list(news_df['content']))
            return news_df
        else:
            print(f"No news found for {ticker} via Yahoo Finance")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error fetching news for {ticker} from Yahoo Finance: {e}")
        return pd.DataFrame()

def save_news_to_csv(news_df, ticker, folder='stock_news'):
    """
    Save news DataFrame to CSV file
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = f"{folder}/{ticker}_news_{datetime.now().strftime('%Y%m%d')}.csv"
    news_df.to_csv(filename, index=False)
    print(f"Saved news for {ticker} to {filename}")

def get_stock_news(tickers, api_key=None, use_yfinance=False, save_to_csv=True):
    """
    Main function to get news for multiple stock tickers
    """
    all_news = pd.DataFrame()
    
    for ticker in tickers:
        print(f"\nFetching news for {ticker}...")
        
        # Try NewsAPI first if API key is provided
        news_df = pd.DataFrame()
        if api_key and not use_yfinance:
            news_df = get_news_from_newsapi(ticker, api_key)
        
        # Fall back to Yahoo Finance if NewsAPI fails or is not available
        if news_df.empty or use_yfinance:
            news_df = get_news_from_yfinance(ticker)
        
        if not news_df.empty:
            all_news = pd.concat([all_news, news_df], ignore_index=True)
            if save_to_csv:
                save_news_to_csv(news_df, ticker)
    
    return all_news

if __name__ == "__main__":
    # Configuration
    STOCK_TICKERS = ['TSLA']  # Add your tickers here
    NEWSAPI_KEY = None   # Get from https://newsapi.org/
    USE_YFINANCE = True                      # Set to True to only use Yahoo Finance
    

    # news_df = get_news_from_newsapi('TSLA', NEWSAPI_KEY)
    # print(news_df)

    # Get news
    news_data = get_stock_news(
        tickers=STOCK_TICKERS,
        api_key=NEWSAPI_KEY,
        use_yfinance=USE_YFINANCE
    )

    # Display summary
    if not news_data.empty:
        print("\nSummary of collected news:")
        print(f"Total articles: {len(news_data)}")
        print("\nLatest headlines:")
      
        for idx, row in news_data.sort_values('publishedAt', ascending=False).head(5).iterrows():
            print(f"{row['publishedAt']} - {row['source']}: {row['title']}")
    else:
        print("No news articles were collected.")