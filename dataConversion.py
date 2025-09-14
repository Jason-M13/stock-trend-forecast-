import numpy as np
from functions import (
    returns,
    volatility,
    trend_indicator,
    bbands_feature,
    check_momentum,
    add_lags,
)

def merge_tables(adx, time_s, b_bands):
    df = time_s.merge(b_bands, left_index = True, right_index = True, how = "inner")
    df = df.merge(adx,left_index = True, right_index = True, how = "inner" )
    return df

def build_features(df):
    df = returns(df, windows=[1, 3, 6, 12], price_col="close")
    df = volatility(df, ret_col="ret_1", window=6)
    df = trend_indicator(df, price_col="close", windows=[10, 20])
    df = bbands_feature(df, upper="upper_band", middle="middle_band", lower="lower_band", price_col="close")
    df = check_momentum(df, price_col="close", momenta=[3, 6])
    df = add_lags(df, cols=("ret_1", "bb_percentage", "adx"), k=1)
    return df

def binary_convert(df, price_col = "close", row = 1):
    #add a shift so that we can compare close from before to today 
    df["next_close"] = df[price_col].shift(-row)
    df["target"] = (df["next_close"] > df[price_col]).astype(int)
    
    if row > 0:
        df = df.iloc[:-row]
    
    df = df.drop(columns = ["next_close"])
    return df
