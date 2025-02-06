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
        st.header(f"{info.get('longName', symbol)} ({symbol})")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Price", f"${info.get('currentPrice', 0):.2f}", 
                     f"{info.get('dayChange', 0):.2f}%")
        with col2:
            market_cap = info.get('marketCap', 0) / 1e9
            st.metric("Market Cap", f"${market_cap:.2f}B")
        with col3:
            pe_ratio = info.get('peRatio', 'N/A')
            pe_display = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
            st.metric("P/E Ratio", pe_display)
        with col4:
            low_52w = info.get('fiftyTwoWeekLow', 0)
            high_52w = info.get('fiftyTwoWeekHigh', 0)
            st.metric("52W Range", f"${low_52w:.2f} - ${high_52w:.2f}")

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
                    f"{info.get('volume', 0):,}",
                    f"{info.get('averageVolume10days', 0):,}",
                    f"{info.get('beta', 'N/A')}",
                    f"${info.get('dayLow', 0):.2f} - ${info.get('dayHigh', 0):.2f}"
                ]
            })
            st.table(stats_df)

        with col2:
            st.markdown("### Financial Metrics")
            metrics_df = pd.DataFrame({
                'Metric': ['Revenue (TTM)', 'Profit Margin', 'Operating Margin', 'ROE'],
                'Value': [
                    f"${info.get('totalRevenue', 0) / 1e9:.2f}B",
                    f"{info.get('profitMargins', 0):.2%}",
                    f"{info.get('operatingMargins', 0):.2%}",
                    f"{info.get('returnOnEquity', 0):.2%}"
                ]
            })
            st.table(metrics_df)

except Exception as e:
    st.error(f"Error: Unable to fetch data for symbol '{symbol}'. Please check if the symbol is correct.")
    st.exception(e)