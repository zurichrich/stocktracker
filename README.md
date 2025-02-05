# Stock Analysis Tool

A Streamlit-based web application for analyzing stock market data with real-time visualization and historical data caching.

## Features

- Real-time stock data visualization
- Technical indicators (Moving Averages)
- Trading volume analysis
- Company information display
- Historical data caching using PostgreSQL
- Interactive charts using Plotly

## Tech Stack

- Python 3.11
- Streamlit
- SQLAlchemy
- PostgreSQL
- YFinance
- Plotly
- Pandas

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
```

4. Initialize the database:
```bash
python create_tables.py
```

5. Run the application:
```bash
streamlit run main.py
```

## Usage

1. Enter a stock symbol (e.g., AAPL, GOOGL)
2. Select the time period for analysis
3. View the interactive price chart with moving averages
4. Analyze trading volume patterns
5. Review key company statistics

## Project Structure

```
├── .streamlit/
│   └── config.toml
├── utils/
│   ├── __init__.py
│   ├── database.py
│   ├── db_operations.py
│   ├── models.py
│   ├── stock_data.py
│   └── visualization.py
├── create_tables.py
├── main.py
└── requirements.txt
```

## Contributing

Feel free to open issues and pull requests for any improvements.

## License

MIT
