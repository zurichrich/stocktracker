import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from . import db_operations
from .database import get_db

def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch stock data from database cache or Yahoo Finance

    Args:
        symbol (str): Stock symbol
        period (str): Time period for data

    Returns:
        pd.DataFrame: DataFrame containing stock data
    """
    try:
        # Convert period to days
        period_days = {
            "1mo": 30,
            "3mo": 90,
            "6mo": 180,
            "1y": 365,
            "2y": 730,
            "5y": 1825
        }
        days = period_days.get(period, 365)

        # Get database session
        db = next(get_db())

        # Try to get cached data
        df = db_operations.get_cached_stock_data(db, symbol, days)

        if df is None:
            # If no cached data, fetch from Yahoo Finance
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)

            # Save to database
            db_operations.save_stock_prices(db, symbol, df)

        # Calculate moving averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()

        return df
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

def get_company_info(symbol: str) -> dict:
    """
    Get company information and key statistics

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Dictionary containing company information
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Calculate day change percentage
        current = info.get('currentPrice', 0)
        previous = info.get('previousClose', 0)
        day_change = ((current - previous) / previous * 100) if previous != 0 else 0

        info['dayChange'] = day_change

        return info
    except Exception as e:
        raise Exception(f"Error fetching company info: {str(e)}")