import os 
import requests
import time 
import pandas as pd 
from dotenv import load_dotenv

class Client:
    @classmethod
    def configure(cls):
        load_dotenv()
        api_key = os.getenv("api_key")
        return cls(api_key)

    def __init__(self, api_key: str, base_url: str = "https://api.twelvedata.com"):
        if not api_key:
            raise ValueError("No API Key")
        self.api_key = api_key
        self.base_url = base_url
        
    def get_adx(self, ticker_symbol, interval):
        url = f"{self.base_url}/adx?symbol={ticker_symbol}&interval={interval}&outputsize=5000&apikey={self.api_key}"
        response = requests.get(url).json()

        values = response["values"]
        df = pd.DataFrame(values)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["adx"] = df["adx"].astype(float)

        #sort/organize
        df = df.sort_values("datetime").set_index("datetime")

        # keep only last 5 years
        cutoff = pd.Timestamp.today() - pd.DateOffset(years=10)
        df = df.loc[df.index >= cutoff]

        return(df)

    def get_bbands(self,ticker_symbol, interval):
        url = f"{self.base_url}/bbands?symbol={ticker_symbol}&interval={interval}&time_period=20&sd=2&outputsize=5000&apikey={self.api_key}"
        response = requests.get(url).json()

        values = response["values"]
        df = pd.DataFrame(values)

        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.astype({
            "upper_band": float,
            "middle_band": float,
            "lower_band": float
        })


        df = df.sort_values("datetime").set_index("datetime")
        cutoff = pd.Timestamp.today() - pd.DateOffset(years=10)
        df = df.loc[df.index >= cutoff]

        return(df)

    def get_tSeries(self, ticker_symbol, interval):
        url = f"{self.base_url}/time_series?symbol={ticker_symbol}&interval={interval}&outputsize=5000&apikey={self.api_key}"
        response = requests.get(url).json()

        values = response["values"]
        df = pd.DataFrame(values)

        df["datetime"] = pd.to_datetime(df["datetime"])
        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col])
        
        df["volume"] = pd.to_numeric(df["volume"]).astype("Int64")

        df = df.sort_values("datetime").set_index("datetime")
        cutoff = pd.Timestamp.today() - pd.DateOffset(years=10)
        df = df.loc[df.index >= cutoff]

        return(df)