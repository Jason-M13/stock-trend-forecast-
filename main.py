import os
from client import configure, get_adx, get_bbands, get_tSeries

if __name__ == "__main__":
    configure()
    ticker = "MSFT"
    api_key = os.getenv("api_key")

    adx = get_adx(ticker,api_key)
    b_bands = get_bbands(ticker,api_key)
    timeSeries = get_tSeries(ticker,api_key)