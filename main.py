import os
from dataConversion import mergeTables, binaryConvert
from client import Client


def run(ticker, interval):  
    client = Client.configure()

    #retrieve data from client 
    adx = client.get_adx(ticker, interval)
    b_bands = client.get_bbands(ticker, interval)
    t_series = client.get_tSeries(ticker, interval)
    
    #data prep
    final_frame = mergeTables(adx, t_series, b_bands)
    convertedFrame = binaryConvert(final_frame)
    print(convertedFrame)

if __name__ == "__main__":
    #Selection
    print("Options: 1day, 1week, 1month")
    interval = input("Choose an interval to train the model with: ")
    ticker   = input("Choose a stock ticker (e.g., AAPL, MSFT): ")

    run(ticker, interval)
