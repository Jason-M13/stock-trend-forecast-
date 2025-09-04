import os 
import requests
import time 
from dotenv import load_dotenv

def configure():
    load_dotenv()

def get_adx(ticker_symbol,api):
    url = f"https://api.twelvedata.com/adx?symbol={ticker_symbol}&interval=1min&apikey={api}"
    response = requests.get(url).json()
   
    latest = response["values"][0]
    adx_value = latest["adx"]
    timestamp = latest["datetime"]
    print(f"{ticker_symbol} ADX: {adx_value} at {timestamp}")



def main():
    configure()
    ticker = "MSFT"
    api_key = os.getenv("api_key")
    get_adx(ticker,api_key)


if __name__ == "__main__":
    main()