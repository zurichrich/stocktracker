import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_price_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create an interactive price chart with moving averages
    
    Args:
        df (pd.DataFrame): DataFrame containing stock data
    
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        )
    )

    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA20'],
            name='20 Day MA',
            line=dict(color='blue', width=1)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA50'],
            name='50 Day MA',
            line=dict(color='orange', width=1)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA200'],
            name='200 Day MA',
            line=dict(color='red', width=1)
        )
    )

    # Update layout
    fig.update_layout(
        title='Stock Price Chart with Moving Averages',
        yaxis_title='Price',
        xaxis_title='Date',
        template='plotly_white',
        height=600,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )

    return fig

def create_volume_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a volume chart
    
    Args:
        df (pd.DataFrame): DataFrame containing stock data
    
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()

    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color='rgb(158,202,225)'
        )
    )

    # Update layout
    fig.update_layout(
        title='Trading Volume',
        yaxis_title='Volume',
        xaxis_title='Date',
        template='plotly_white',
        height=300,
        showlegend=False
    )

    return fig
