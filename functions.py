import pandas as pd
import numpy as np

def returns(table, windows = [1,3,6,12], price_col ="close"):
    for i in windows:
        table[f"ret_{i}"] = table[price_col] / table[price_col].shift(i)-1
        
    return table

def volatility(table, ret_col = "ret_1", window = 6):
    table[f"vol_{window}"] = table[ret_col].rolling(window).std()
    return table

def trend_indicator(table, price_col = "close", windows = [10,20]):
    for i in windows:
        sma = table[price_col].rolling(i).mean()
        table[f"sma_{i}"] = sma
        table[f"close_over_sma{i}"] = table[price_col]/sma
    return table

def bbands_feature(table, upper = "upper_band", middle = "middle_band", lower = "lower_band", price_col = "close"):
    denominator = table[upper] - table[lower]
    table["bb_percentage"] = (table[price_col] - table[lower])/denominator
    table["bb_width"] = denominator/table[middle]
    return table

def check_momentum(table, price_col = "close", momenta = [3,6]):
    for i in momenta:
        table[f"momentum_{i}"] = table[price_col] - table[price_col].shift(i)
    return table

def add_lags(table, cols = ("ret_1","bb_percentage", "adx"), k = 1):
    for i in cols:
        if i in table.columns:
            table[f"{i}_lag{k}"] = table[i].shift(k)
    return table

