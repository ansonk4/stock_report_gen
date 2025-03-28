import os
from datetime import date
from dataclasses import dataclass
from typing import List
from openai import OpenAI
import news
import get_price
from dotenv import load_dotenv

@dataclass
class Config:
    """Configuration settings for the application"""
    load_dotenv()
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = "https://openrouter.ai/api/v1"
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")
    MODEL_NAME: str = "deepseek/deepseek-chat-v3-0324:free"

class NewsFormatter:
    @staticmethod
    def format_news_items(news_df) -> str:
        """Format news items into a string with webpage markers"""
        news_items = []
        for idx, row in news_df.iterrows():
            news_items.append(
                f"[webpage {idx} begin] "
                f"Date: {row['pubDate']} - "
                f"Title: {row['title']} - "
                f"Summary: {row['summary']} "
                f"[webpage {idx} end]"
            )
        news_str = "\n".join(news_items)

        citation = " \n\n".join([f"Citation:{idx}: {row['canonicalUrl']['url']}" for idx, row in news_df.iterrows()])

        return news_str, citation

class ReportGenerator:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY
        )

    def _create_prompt(self, stock: str, news_content: str, price_info: str) -> str:
        """Create the prompt for the AI model"""
        question = (
            f"Generate a report summaring news for the stock {stock} for the last week, "
            f"if there is a significant price change, please include focus on news on that date. "
            f"Below is the price information for the last week: {price_info}"
        )

        return f"""# The following contents are the search results related to the user's message:
                {news_content}
                In the search results I provide to you, each result is formatted as [webpage X begin]...[webpage X end], 
                where X represents the numerical index of each article. Please cite the context at the end of the relevant 
                sentence when appropriate. Use the citation format [citation:X] in the corresponding part of your answer. 
                If a sentence is derived from multiple contexts, list all relevant citation numbers, such as [citation:3][citation:5]. 
                Be sure not to cluster all citations at the end; instead, include them in the corresponding parts of the answer.

                When responding, please keep the following points in mind:
                - Today is {date.today()}.
                - Not all content in the search results is closely related to the user's question.
                - Format the response with clear structure and proper citations.
                - Synthesize information from multiple sources.
                - Focus on the most relevant and important information.
                - When using a dollar sign, add a slash before it like this '\$' 
                # The user's message is:
                {question}"""

    def generate_report(self, stock: str, report=True) -> str:
        """Generate a complete stock report"""
        # Fetch data
        news_data = news.get_news_from_yfinance(stock)
        price_data = get_price.get_last_week_prices(stock)

        # Format news data
        formatted_news, citations = NewsFormatter.format_news_items(news_data)
        
        # Create prompt and get AI response
        prompt = self._create_prompt(stock, formatted_news, price_data)
        
        if report:
            completion = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                extra_body={}
            )
        else:
            return "{report}", citations

        return completion.choices[0].message.content, citations

def main():
    config = Config()
    generator = ReportGenerator(config)
    stock_symbol = "TSLA"
    
    try:
        report = generator.generate_report(stock_symbol)
        print(report)
    except Exception as e:
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    # Ensure environment variables are set
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("NEWSAPI_KEY"):
        print("Error: Missing required environment variables OPENAI_API_KEY or NEWSAPI_KEY.")
    else:
        main()