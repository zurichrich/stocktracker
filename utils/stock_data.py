import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        symbol (str): Stock symbol
        period (str): Time period for data
    
    Returns:
        pd.DataFrame: DataFrame containing stock data
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        
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
