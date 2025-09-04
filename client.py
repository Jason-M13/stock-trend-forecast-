import os 
import requests
import time 
import pandas as pd 
from dotenv import load_dotenv

def configure():
    load_dotenv()

def get_adx(ticker_symbol,api):
    url = f"https://api.twelvedata.com/adx?symbol={ticker_symbol}&interval=1month&outputsize=5000&apikey={api}"
    response = requests.get(url).json()

    values = response["values"]
    df = pd.DataFrame(values)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["adx"] = df["adx"].astype(float)

    #sort/organize
    df = df.sort_values("datetime").set_index("datetime")

    # keep only last 5 years
    cutoff = pd.Timestamp.today() - pd.DateOffset(years=5)
    df = df.loc[df.index >= cutoff]

    return(df)


def get_bbands(ticker_symbol,api):
    url = f"https://api.twelvedata.com/bbands?symbol={ticker_symbol}&interval=1month&time_period=20&sd=2&outputsize=5000&apikey={api}"
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
    cutoff = pd.Timestamp.today() - pd.DateOffset(years=5)
    df = df.loc[df.index >= cutoff]

    return(df)

    

def get_tSeries(ticker_symbol,api):
    url = f"https://api.twelvedata.com/time_series?symbol={ticker_symbol}&interval=1month&outputsize=5000&apikey={api}"
    response = requests.get(url).json()

    values = response["values"]
    df = pd.DataFrame(values)

    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col])
    
    df["volume"] = pd.to_numeric(df["volume"]).astype("Int64")

    df = df.sort_values("datetime").set_index("datetime")
    cutoff = pd.Timestamp.today() - pd.DateOffset(years=5)
    df = df.loc[df.index >= cutoff]

    return(df)