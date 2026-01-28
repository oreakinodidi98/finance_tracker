# main_agent/stock_data_manager.py

import requests
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class StockDataManager:
    """Manages stock data retrieval from Alpha Vantage API."""
    
    def __init__(self, api_key: str):
        """
        Initialize StockDataManager.
        
        :param api_key: Alpha Vantage API key
        """
        self._api_key = api_key
        self._base_url = "https://www.alphavantage.co/query"
    
    def get_stock_data(
        self, 
        symbol: str, 
        interval: str = "5min", 
        outputsize: str = "compact"
    ) -> str:
        """
        Get real-time and historical stock price data from Alpha Vantage API.
        
        :param symbol: Stock ticker symbol (e.g., IBM, AAPL, TSLA)
        :param interval: Time interval (1min, 5min, 15min, 30min, 60min)
        :param outputsize: Data size ('compact' or 'full')
        :return: Formatted stock data string
        """
        try:
            # Validate interval
            valid_intervals = ["1min", "5min", "15min", "30min", "60min"]
            if interval not in valid_intervals:
                return f"Invalid interval '{interval}'. Must be one of: {', '.join(valid_intervals)}"
            
            # Build API request parameters
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol.upper(),
                "interval": interval,
                "apikey": self._api_key,
                "outputsize": outputsize,
                "adjusted": "true",
                "extended_hours": "false"  # Regular trading hours only
            }
            
            print(f"📈 Fetching stock data for {symbol.upper()}...")
            
            # Make API request
            response = requests.get(self._base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                return f"Error: {data['Error Message']}. Please check the stock symbol."
            
            if "Note" in data:
                return f"API rate limit reached: {data['Note']}. Please try again in a moment."
            
            if "Information" in data:
                return f"API Info: {data['Information']}"
            
            # Extract metadata and time series
            meta_data = data.get("Meta Data", {})
            time_series_key = f"Time Series ({interval})"
            time_series = data.get(time_series_key, {})
            
            if not time_series:
                return f"No data found for {symbol}. The symbol may be invalid or data may not be available."
            
            # Format the response
            return self._format_stock_data(symbol, interval, meta_data, time_series)
            
        except requests.exceptions.Timeout:
            return f"Request timeout while fetching data for {symbol}. Please try again."
        except requests.exceptions.RequestException as e:
            return f"Error fetching stock data: {str(e)}"
        except Exception as e:
            return f"Unexpected error retrieving stock data for {symbol}: {str(e)}"
    
    def _format_stock_data(
        self, 
        symbol: str, 
        interval: str, 
        meta_data: dict, 
        time_series: dict
    ) -> str:
        """
        Format stock data into a readable string.
        
        :param symbol: Stock symbol
        :param interval: Time interval
        :param meta_data: API metadata
        :param time_series: Time series data
        :return: Formatted string
        """
        symbol_name = meta_data.get("2. Symbol", symbol)
        last_refreshed = meta_data.get("3. Last Refreshed", "N/A")
        
        result = f"Stock Data for {symbol_name}\n"
        result += f"Last Updated: {last_refreshed}\n"
        result += f"Interval: {interval}\n\n"
        
        # Get the most recent 5 data points
        recent_data = list(time_series.items())[:5]
        
        result += "Recent Price Data:\n"
        for timestamp, values in recent_data:
            open_price = values.get("1. open", "N/A")
            high_price = values.get("2. high", "N/A")
            low_price = values.get("3. low", "N/A")
            close_price = values.get("4. close", "N/A")
            volume = values.get("5. volume", "N/A")
            
            result += f"\n{timestamp}:\n"
            result += f"  Open: ${open_price}\n"
            result += f"  High: ${high_price}\n"
            result += f"  Low: ${low_price}\n"
            result += f"  Close: ${close_price}\n"
            result += f"  Volume: {volume}\n"
        
        # Add a summary of the latest price
        if recent_data:
            latest_time, latest_values = recent_data[0]
            latest_close = latest_values.get("4. close", "N/A")
            result += f"\n💰 Current Price: ${latest_close}"
        
        return result