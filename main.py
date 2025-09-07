import os
#from dataConversion import prepFrame
from client import Client


def run(ticker, interval):  
    client = Client.configure()


if __name__ == "__main__":
    #Selection
    print("Options: 1day, 1week, 1month")
    interval = input("Choose an interval to train the model with: ")
    ticker   = input("Choose a stock ticker (e.g., AAPL, MSFT): ")

    run(ticker, interval)
