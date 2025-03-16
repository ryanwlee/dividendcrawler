import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import yfinance as yf
import time
import os

class YieldMaxCrawler:
    def __init__(self):
        self.base_url = "https://www.yieldmaxetfs.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Load existing data if available
        self.existing_data = self.load_existing_data()
        # Dictionary of ETF symbols and their paths
        self.etf_paths = {
            'TSLY': '/our-etfs/tsly/',  # TSLA Option Income
            'OARK': '/our-etfs/oark/',  # Innovation Option Income
            'APLY': '/our-etfs/aply/',  # AAPL Option Income
            'NVDY': '/our-etfs/nvdy/',  # NVDA Option Income
            'AMZY': '/our-etfs/amzy/',  # AMZN Option Income
            'FBY': '/our-etfs/fby/',  # META Option Income
            'GOOY': '/our-etfs/gooy/',  # GOOGL Option Income
            'CONY': '/our-etfs/cony/',  # COIN Option Income
            'NFLY': '/our-etfs/nfly/',  # NFLX Option Income
            'DISO': '/our-etfs/diso/',  # DIS Option Income
            'MSFO': '/our-etfs/msfo/',  # MSFT Option Income
            'XOMO': '/our-etfs/xomo/',  # XOM Option Income
            'JPMO': '/our-etfs/jpmo/',  # JPM Option Income
            'AMDY': '/our-etfs/amdy/',  # AMD Option Income
            'PYPY': '/our-etfs/pypy/',  # PYPL Option Income
            'SQY': '/our-etfs/sqy/',  # XYZ Option Income
            'MRNY': '/our-etfs/mrny/',  # MRNA Option Income
            'AIYY': '/our-etfs/aiyy/',  # AI Option Income
            'MSTY': '/our-etfs/msty/',  # MSTR Option Income
            'YBIT': '/our-etfs/ybit-bitcoin-option-income-etf/',  # Bitcoin Option Income
            'GDXY': '/our-etfs/gdxy/',  # Gold Miners Option Income
            'SNOY': '/our-etfs/snoy/',  # SNOW Option Income
            'ABNY': '/our-etfs/abny/',  # ABNB Option Income
            'BABO': '/our-etfs/babo/',  # BABA Option Income
            'TSMY': '/our-etfs/tsmy/',  # TSM Option Income
            'SMCY': '/our-etfs/smcy/',  # SMCI Option Income
            'PLTY': '/our-etfs/plty/',  # PLTR Option Income
            'MARO': '/our-etfs/maro/',  # MARA Option Income
            'CVNY': '/our-etfs/cvny/',  # CVNA Option Income
            'YMAX': '/our-etfs/ymax/',  # Universe FoF
            'YMAG': '/our-etfs/ymag/',  # Magnificent 7 FoF
            'FIVY': '/our-etfs/fivy/',  # Dorsey Wright Hybrid 5 Income
            'FEAT': '/our-etfs/feat/',  # Dorsey Wright Featured 5 Income
            'ULTY': '/our-etfs/ulty/',  # Ultra Option Income
            'CRSH': '/our-etfs/crsh/',  # Short TSLA Option Income
            'FIAT': '/our-etfs/fiat/',  # Short COIN Option Income
            'DIPS': '/our-etfs/dips/',  # Short NVDA Option Income
            'YQQQ': '/our-etfs/yqqq/',  # Short N100 Option Income
            'BIGY': '/our-etfs/bigy/',  # Target 12™ Big 50 Option Income
            'SOXY': '/our-etfs/soxy/',  # Target 12™ Semiconductor Option Income
            'LFGY': '/our-etfs/lfgy/',  # Crypto Portfolio Option Income
            'GPTY': '/our-etfs/gpty/',  # Al & Tech Portfolio Option Income
            'SDTY': '/our-etfs/sdty/',  # S&P 500 0DTE Option Income
            'QDTY': '/our-etfs/qdty/',  # Nasdaq 100 0DTE Option Income
            'RDTY': '/our-etfs/rdty/',  # R2000 0DTE Option Income
        }
        # Dictionary mapping YieldMax ETFs to their underlying stock symbols
        self.underlying_symbols = {
            'TSLY': 'TSLA',  # Tesla
            'APLY': 'AAPL',  # Apple
            'NVDY': 'NVDA',  # NVIDIA
            'AMZY': 'AMZN',  # Amazon
            'FBY': 'META',   # Meta (Facebook)
            'GOOY': 'GOOGL', # Google
            'CONY': 'COIN',  # Coinbase
            'NFLY': 'NFLX',  # Netflix
            'DISO': 'DIS',   # Disney
            'MSFO': 'MSFT',  # Microsoft
            'XOMO': 'XOM',   # Exxon Mobil
            'JPMO': 'JPM',   # JPMorgan
            'AMDY': 'AMD',   # AMD
            'PYPY': 'PYPL',  # PayPal
            'MRNY': 'MRNA',  # Moderna
            'MSTY': 'MSTR',  # MicroStrategy
            'SNOY': 'SNOW',  # Snowflake
            'ABNY': 'ABNB',  # Airbnb
            'BABO': 'BABA',  # Alibaba
            'TSMY': 'TSM',   # TSMC
            'SMCY': 'SMCI',  # Super Micro Computer
            'PLTY': 'PLTR',  # Palantir
            'MARO': 'MARA',  # Marathon Digital
            'CVNY': 'CVNA',  # Carvana
        }

    def load_existing_data(self, filename='yieldmax_etf_distribution.json'):
        """Load existing distribution data from JSON file if it exists."""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_existing_price(self, symbol, date_str):
        """Check if we already have the price data in our existing data."""
        if not self.existing_data:
            return None

        for etf_data in self.existing_data:
            if not etf_data.get('distributions'):
                continue

            for dist in etf_data['distributions']:
                # Check ETF prices
                if dist.get('etf_price_declared', {}).get('symbol') == symbol and \
                   dist.get('etf_price_declared', {}).get('date') == date_str:
                    return dist['etf_price_declared']
                
                if dist.get('etf_price_ex', {}).get('symbol') == symbol and \
                   dist.get('etf_price_ex', {}).get('date') == date_str:
                    return dist['etf_price_ex']
                
                # Check underlying stock prices
                if dist.get('underlying_stock_price_declared', {}).get('symbol') == symbol and \
                   dist.get('underlying_stock_price_declared', {}).get('date') == date_str:
                    return dist['underlying_stock_price_declared']
                
                if dist.get('underlying_stock_price_ex', {}).get('symbol') == symbol and \
                   dist.get('underlying_stock_price_ex', {}).get('date') == date_str:
                    return dist['underlying_stock_price_ex']
        
        return None

    def get_etf_list(self):
        """Fetch the list of all available ETFs from the main page."""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all ETF links in the Covered Call ETFs section
            etf_links = {}
            covered_call_section = soup.find('a', string=lambda x: x and 'Covered Call ETFs' in x)
            if covered_call_section:
                etf_list = covered_call_section.find_next('ul')
                if etf_list:
                    for link in etf_list.find_all('a'):
                        text = link.text.strip()
                        if '(' in text and ')' in text:
                            symbol = text.split('(')[0].strip()
                            href = link.get('href')
                            if href:
                                etf_links[symbol] = href
            
            return etf_links
        except Exception as e:
            print(f"Error fetching ETF list: {e}")
            return {}

    def is_valid_money_amount(self, amount):
        """Check if string is a valid money amount."""
        try:
            amount = amount.replace(',', '')
            value = float(amount)
            return value >= 0  # Money amount should be positive
        except ValueError:
            return False

    def is_valid_date(self, date_str):
        """Check if string matches date format MM/DD/YYYY."""
        try:
            datetime.strptime(date_str, '%m/%d/%Y')
            return True
        except ValueError:
            return False

    def validate_distribution_data(self, distribution):
        """Validate all fields in a distribution entry."""
        errors = []
        
        # Check Distribution per Share
        if not self.is_valid_money_amount(distribution["Distribution per Share"]):
            errors.append(f"Invalid money amount: {distribution['Distribution per Share']}")

        # Check all date fields
        date_fields = ["declared date", "ex date", "record date", "payable date"]
        for field in date_fields:
            if not self.is_valid_date(distribution[field]):
                errors.append(f"Invalid date format for {field}: {distribution[field]}")

        return errors

    def fetch_page(self, etf_symbol):
        """Fetch page for a specific ETF."""
        try:
            if etf_symbol not in self.etf_paths:
                print(f"ETF symbol {etf_symbol} not found in known paths")
                return None
                
            path = self.etf_paths[etf_symbol]
            # Remove any full URLs from the path
            if 'https://' in path:
                path = path.split('www.yieldmaxetfs.com')[1]
            
            url = self.base_url + path
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching page for {etf_symbol}: {e}")
            return None

    def get_stock_price(self, symbol, date_str):
        """Get stock price for a specific date using Yahoo Finance API."""
        try:
            # Check if we already have this price in our existing data
            existing_price = self.get_existing_price(symbol, date_str)
            if existing_price:
                return {
                    "open": existing_price["open"],
                    "high": existing_price["high"],
                    "low": existing_price["low"],
                    "close": existing_price["close"],
                    "volume": existing_price["volume"]
                }

            # Convert date string to datetime
            date = pd.to_datetime(date_str)
            timestamp = int(date.timestamp())
            
            # Yahoo Finance API endpoint
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                "period1": timestamp - 86400,  # One day before
                "period2": timestamp + 86400,  # One day after
                "interval": "1d",
                "events": "history"
            }
            
            # Add delay to avoid rate limiting
            time.sleep(0.5)
            
            response = requests.get(url, params=params, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to get data for {symbol} on {date_str}: HTTP {response.status_code}")
                return None
                
            data = response.json()
            if "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                print(f"No data available for {symbol} on {date_str}")
                return None
                
            result = data["chart"]["result"][0]
            timestamps = result["timestamp"]
            quote = result["indicators"]["quote"][0]
            
            # Find the closest date
            target_timestamp = timestamp
            closest_idx = min(range(len(timestamps)), 
                            key=lambda i: abs(timestamps[i] - target_timestamp))
            
            return {
                "open": float(quote["open"][closest_idx]),
                "high": float(quote["high"][closest_idx]),
                "low": float(quote["low"][closest_idx]),
                "close": float(quote["close"][closest_idx]),
                "volume": int(quote["volume"][closest_idx])
            }
            
        except Exception as e:
            print(f"Error fetching stock price for {symbol} on {date_str}: {str(e)}")
            return None

    def extract_distribution_details(self, soup, etf_symbol):
        """Extract distribution details for a specific ETF."""
        try:
            distributions = []
            # Look for the Distribution Details section specifically
            distribution_section = soup.find('h2', string='Distribution Details')
            if not distribution_section:
                print(f"Could not find Distribution Details section for {etf_symbol}")
                return None
                
            # Find the table that follows the Distribution Details heading
            table = distribution_section.find_next('table')
            if not table:
                print(f"Could not find Distribution Details table for {etf_symbol}")
                return None

            # Skip header row by starting from index 1
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 6:  # We expect 6 columns (including ticker name)
                    distribution = {
                        "symbol": etf_symbol,
                        "Distribution per Share": cols[1].text.strip(),
                        "declared date": cols[2].text.strip(),
                        "ex date": cols[3].text.strip(),
                        "record date": cols[4].text.strip(),
                        "payable date": cols[5].text.strip()
                    }
                    
                    # Validate the data before adding
                    validation_errors = self.validate_distribution_data(distribution)
                    if validation_errors:
                        print(f"Validation errors found for {etf_symbol}:")
                        for error in validation_errors:
                            print(f"  - {error}")
                        print("Skipping this distribution entry")
                        continue
                    
                    # Get ETF's own stock price for declared and ex dates
                    etf_declared_price = self.get_stock_price(etf_symbol, distribution["declared date"])
                    etf_ex_price = self.get_stock_price(etf_symbol, distribution["ex date"])
                    
                    if etf_declared_price:
                        distribution["etf_price_declared"] = {
                            "symbol": etf_symbol,
                            "date": distribution["declared date"],
                            **etf_declared_price
                        }
                    
                    if etf_ex_price:
                        distribution["etf_price_ex"] = {
                            "symbol": etf_symbol,
                            "date": distribution["ex date"],
                            **etf_ex_price
                        }
                        
                        # Calculate dividend yields if we have both distribution amount and ex-date price
                        try:
                            dist_amount = float(distribution["Distribution per Share"].replace(',', ''))
                            ex_price = etf_ex_price["close"]
                            
                            if ex_price > 0:
                                monthly_yield = (dist_amount / ex_price)
                                yearly_yield = monthly_yield * 12
                                
                                distribution["monthly_dividend_yield"] = round(monthly_yield * 100, 2)  # Convert to percentage
                                distribution["yearly_dividend_yield"] = round(yearly_yield * 100, 2)    # Convert to percentage
                        except (ValueError, KeyError) as e:
                            print(f"Could not calculate dividend yields for {etf_symbol}: {str(e)}")
                    
                    # Add underlying stock price data if available
                    underlying_symbol = self.underlying_symbols.get(etf_symbol)
                    if underlying_symbol:
                        # Get stock price for declared date and ex date
                        declared_price = self.get_stock_price(underlying_symbol, distribution["declared date"])
                        ex_price = self.get_stock_price(underlying_symbol, distribution["ex date"])
                        
                        if declared_price:
                            distribution["underlying_stock_price_declared"] = {
                                "symbol": underlying_symbol,
                                "date": distribution["declared date"],
                                **declared_price
                            }
                        
                        if ex_price:
                            distribution["underlying_stock_price_ex"] = {
                                "symbol": underlying_symbol,
                                "date": distribution["ex date"],
                                **ex_price
                            }
                        
                    distributions.append(distribution)
            
            if not distributions:
                print(f"No valid distribution data found for {etf_symbol}")
                return None

            # Add timestamp for tracking when the data was collected
            result = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "symbol": etf_symbol,
                "underlying_symbol": self.underlying_symbols.get(etf_symbol),
                "distributions": distributions
            }
            
            return result
        except Exception as e:
            print(f"Error extracting distribution details for {etf_symbol}: {e}")
            return None

    def save_to_json(self, data_list, filename='frontend/src/data/yieldmax_etf_distribution.json'):
        """Save multiple ETF data to JSON file."""
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            # Save data directly, overwriting any existing file
            with open(filename, 'w') as f:
                json.dump(data_list, f, indent=2)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to JSON: {e}")

    def save_successful_etfs(self, successful_etfs, filename='frontend/src/data/yieldmax_etf_successful.json'):
        """Save list of successfully crawled ETFs."""
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            data = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "successful_etfs": [
                    {
                        "symbol": symbol,
                        "name": self.etf_paths[symbol].split('/')[-2].upper(),  # Extract name from path
                        "distributions_count": len(etf_data["distributions"])
                    }
                    for symbol, etf_data in successful_etfs.items()
                ]
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Successfully crawled ETFs list saved to {filename}")
        except Exception as e:
            print(f"Error saving successful ETFs list: {e}")

    def run(self, symbols=None):
        """Run the crawler for specified ETFs or all known ETFs."""
        print("Starting YieldMax ETF crawler...")
        
        # If no symbols provided, use all known ETFs
        if symbols is None:
            # Get the list of ETFs from the main page
            etf_paths = self.get_etf_list()
            self.etf_paths.update(etf_paths)
            symbols = list(self.etf_paths.keys())

        all_data = []
        successful_etfs = {}  # Track successfully crawled ETFs
        
        for symbol in symbols:
            print(f"Processing {symbol}...")
            soup = self.fetch_page(symbol)
            if soup:
                distribution_data = self.extract_distribution_details(soup, symbol)
                if distribution_data and distribution_data["distributions"]:  # Only if we have valid distributions
                    all_data.append(distribution_data)
                    successful_etfs[symbol] = distribution_data  # Track successful ETF
                    print(f"Successfully processed {symbol}")
                else:
                    print(f"Failed to extract distribution details for {symbol}")
            else:
                print(f"Failed to fetch webpage for {symbol}")

        if all_data:
            self.save_to_json(all_data)
            self.save_successful_etfs(successful_etfs)
            print("Crawling completed successfully!")
        else:
            print("Failed to extract any distribution details.")

if __name__ == "__main__":
    crawler = YieldMaxCrawler()
    # Run for all ETFs
    crawler.run() 