from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta
import pandas as pd

def get_or_create_stock(db: Session, symbol: str) -> models.Stock:
    """Get or create a stock record"""
    stock = db.query(models.Stock).filter(models.Stock.symbol == symbol).first()
    if not stock:
        stock = models.Stock(symbol=symbol)
        db.add(stock)
        db.commit()
        db.refresh(stock)
    return stock

def save_stock_prices(db: Session, symbol: str, df: pd.DataFrame):
    """Save stock prices to database"""
    stock = get_or_create_stock(db, symbol)
    
    for index, row in df.iterrows():
        price = models.StockPrice(
            stock_id=stock.id,
            date=index,
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=row['Volume']
        )
        db.add(price)
    
    db.commit()

def get_cached_stock_data(db: Session, symbol: str, days: int) -> pd.DataFrame:
    """Get cached stock data from database"""
    stock = get_or_create_stock(db, symbol)
    cutoff_date = datetime.now() - timedelta(days=days)
    
    prices = (db.query(models.StockPrice)
             .filter(models.StockPrice.stock_id == stock.id)
             .filter(models.StockPrice.date >= cutoff_date)
             .all())
    
    if not prices:
        return None
        
    data = {
        'Open': [p.open for p in prices],
        'High': [p.high for p in prices],
        'Low': [p.low for p in prices],
        'Close': [p.close for p in prices],
        'Volume': [p.volume for p in prices]
    }
    
    df = pd.DataFrame(data, index=[p.date for p in prices])
    return df
