import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from . import db_operations
from .database import get_db
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch stock data from database cache or Yahoo Finance with improved error handling
    """
    try:
        # Validate input
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid stock symbol")

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
        logger.info(f"Fetching data for {symbol} for period {period}")

        try:
            # Try to get cached data
            df = db_operations.get_cached_stock_data(db, symbol, days)

            if df is not None and not df.empty:
                logger.info("Using cached data")
                # Calculate moving averages
                df['MA20'] = df['Close'].rolling(window=20).mean()
                df['MA50'] = df['Close'].rolling(window=50).mean()
                df['MA200'] = df['Close'].rolling(window=200).mean()
                return df

            # If no cached data, fetch from Yahoo Finance with retry mechanism
            logger.info("Fetching fresh data from Yahoo Finance")
            max_retries = 3
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    stock = yf.Ticker(symbol)
                    df = stock.history(period=period)

                    if df.empty:
                        raise ValueError(f"No data available for symbol {symbol}")

                    # Validate data
                    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    if not all(col in df.columns for col in required_columns):
                        raise ValueError(f"Missing required columns in data for {symbol}")

                    # Save to database in chunks to prevent memory issues
                    chunk_size = 1000
                    for i in range(0, len(df), chunk_size):
                        chunk = df.iloc[i:i + chunk_size]
                        db_operations.save_stock_prices(db, symbol, chunk)

                    # Calculate moving averages
                    df['MA20'] = df['Close'].rolling(window=20).mean()
                    df['MA50'] = df['Close'].rolling(window=50).mean()
                    df['MA200'] = df['Close'].rolling(window=200).mean()

                    return df

                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Retry {attempt + 1}/{max_retries} failed: {str(e)}")
                        time.sleep(retry_delay)
                        continue
                    raise

        except Exception as e:
            logger.error(f"Database operation error: {str(e)}")
            raise

    except Exception as e:
        error_msg = f"Unable to fetch data for {symbol}: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

def get_company_info(symbol: str) -> dict:
    """
    Get company information with improved error handling and retry mechanism
    """
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            if not info:
                raise ValueError(f"No information available for symbol {symbol}")

            # Validate required fields
            required_fields = ['currentPrice', 'previousClose', 'marketCap', 'volume']
            for field in required_fields:
                if field not in info:
                    info[field] = 0
                    logger.warning(f"Missing {field} in company info for {symbol}")

            # Calculate day change percentage with proper error handling
            try:
                current = info.get('currentPrice', 0)
                previous = info.get('previousClose', 0)
                day_change = ((current - previous) / previous * 100) if previous != 0 else 0
                info['dayChange'] = day_change
            except Exception as e:
                logger.warning(f"Error calculating day change: {str(e)}")
                info['dayChange'] = 0

            return info

        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Retry {attempt + 1}/{max_retries} failed: {str(e)}")
                time.sleep(retry_delay)
                continue
            error_msg = f"Unable to fetch company info for {symbol}: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)