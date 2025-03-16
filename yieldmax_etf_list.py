import requests
from bs4 import BeautifulSoup
import json

class ETFListCrawler:
    def __init__(self):
        self.base_url = "https://www.yieldmaxetfs.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_all_etfs(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            etf_data = {}
            
            # Find all ETF category sections
            etf_categories = soup.find_all('a', href=lambda x: x and 'our-etfs' in x)
            
            for category in etf_categories:
                category_name = category.text.strip()
                # Find the list of ETFs that follows this category
                etf_list = category.find_next('ul')
                if etf_list:
                    for link in etf_list.find_all('a'):
                        text = link.text.strip()
                        if '(' in text and ')' in text:
                            # Extract symbol and full name
                            symbol = text.split('(')[0].strip()
                            full_name = text.split('(')[1].replace(')', '').strip()
                            href = link.get('href')
                            if href:
                                etf_data[symbol] = {
                                    'url': href if href.startswith('/') else '/' + href,
                                    'name': full_name,
                                    'category': category_name
                                }
            
            return etf_data
        except Exception as e:
            print(f"Error fetching ETF list: {e}")
            return {}

    def save_to_json(self, data, filename='yieldmax_etf_list.json'):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"ETF list saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

    def generate_etf_paths_code(self, data):
        """Generate code snippet for etf_paths dictionary."""
        code = "self.etf_paths = {\n"
        for symbol, info in data.items():
            code += f"    '{symbol}': '{info['url']}',  # {info['name']}\n"
        code += "}"
        return code

    def run(self):
        print("Fetching ETF list from YieldMax...")
        etf_data = self.get_all_etfs()
        
        if etf_data:
            # Save full data to JSON
            self.save_to_json(etf_data)
            
            # Generate and save code snippet
            code_snippet = self.generate_etf_paths_code(etf_data)
            with open('yieldmax_etf_list_snippet.txt', 'w') as f:
                f.write(code_snippet)
            print("Code snippet saved to yieldmax_etf_list_snippet.txt")
            
            print(f"\nFound {len(etf_data)} ETFs")
            print("\nExample of generated code snippet:")
            print(code_snippet[:200] + "...")
        else:
            print("Failed to fetch ETF list")

if __name__ == "__main__":
    crawler = ETFListCrawler()
    crawler.run() 