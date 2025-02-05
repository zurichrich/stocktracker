import streamlit as st
import yfinance as yf
from utils.stock_data import get_stock_data, get_company_info
from utils.visualization import create_price_chart, create_volume_chart
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Stock Analysis Tool")
st.markdown("""
This application provides real-time stock analysis and visualization tools.
Enter a stock symbol to get started!
""")

# Stock symbol input
col1, col2 = st.columns([2, 1])
with col1:
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL)", "AAPL").upper()
with col2:
    period = st.selectbox(
        "Select Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )

try:
    # Get stock data
    df = get_stock_data(symbol, period)
    info = get_company_info(symbol)
    
    if df is not None and not df.empty:
        # Company information section
        st.header(f"{info['longName']} ({symbol})")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${info['currentPrice']:.2f}", 
                     f"{info['dayChange']:.2f}%")
        with col2:
            st.metric("Market Cap", f"${info['marketCap'] / 1e9:.2f}B")
        with col3:
            st.metric("P/E Ratio", f"{info['peRatio']:.2f}")
        with col4:
            st.metric("52W Range", f"${info['fiftyTwoWeekLow']:.2f} - ${info['fiftyTwoWeekHigh']:.2f}")

        # Charts
        st.subheader("Price Chart")
        fig = create_price_chart(df)
        st.plotly_chart(fig, use_container_width=True)

        # Volume Chart
        st.subheader("Trading Volume")
        volume_fig = create_volume_chart(df)
        st.plotly_chart(volume_fig, use_container_width=True)

        # Key Statistics
        st.header("Key Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Trading Information")
            stats_df = pd.DataFrame({
                'Metric': ['Volume', 'Avg Volume (10d)', 'Beta', 'Days Range'],
                'Value': [
                    f"{info['volume']:,}",
                    f"{info['averageVolume10days']:,}",
                    f"{info['beta']:.2f}",
                    f"${info['dayLow']:.2f} - ${info['dayHigh']:.2f}"
                ]
            })
            st.table(stats_df)

        with col2:
            st.markdown("### Financial Metrics")
            metrics_df = pd.DataFrame({
                'Metric': ['Revenue (TTM)', 'Profit Margin', 'Operating Margin', 'ROE'],
                'Value': [
                    f"${info['totalRevenue'] / 1e9:.2f}B",
                    f"{info['profitMargins']:.2%}",
                    f"{info['operatingMargins']:.2%}",
                    f"{info['returnOnEquity']:.2%}"
                ]
            })
            st.table(metrics_df)

except Exception as e:
    st.error(f"Error: Unable to fetch data for symbol '{symbol}'. Please check if the symbol is correct.")
    st.exception(e)
