from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# Association table for watchlist
watchlist = Table(
    'watchlist',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('stock_id', Integer, ForeignKey('stocks.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    stocks = relationship("Stock", secondary=watchlist, back_populates="users")

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    users = relationship("User", secondary=watchlist, back_populates="stocks")
    prices = relationship("StockPrice", back_populates="stock")

class StockPrice(Base):
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    
    stock = relationship("Stock", back_populates="prices")
