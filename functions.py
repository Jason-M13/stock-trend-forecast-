import pandas as pd
import numpy as np

def returns(table, windows=[1, 3, 6, 12], price_col="close"):
    """
    Compute the percentage returns over specified lookback windows.
    
    Args:
        table (pd.DataFrame): Input DataFrame containing price data.
        windows (list[int], optional): List of lookback periods (in rows) 
            for which to calculate returns. Default is [1, 3, 6, 12].
        price_col (str, optional): Column name for the price series.
            Default is "close".

    Returns:
        pd.DataFrame: Original DataFrame with new return columns added,
            named 'ret_{window}' for each window.

    Raises:
        KeyError: If `price_col` is not found in the DataFrame.
    """
    try:
        if price_col not in table.columns:
            raise KeyError(f"Column '{price_col}' not found in DataFrame")

        for i in windows:
            table[f"ret_{i}"] = table[price_col] / table[price_col].shift(i) - 1

    except Exception as e:
        print(f"[returns] Error: {e}")
    return table

def volatility(table, ret_col="ret_1", window=6):
    """
    Calculate rolling the standard deviation of returns (volatility).

    Args:
        table (pd.DataFrame): Input DataFrame containing return data.
        ret_col (str): Column name of returns to use. Default is "ret_1".
        window (int): Rolling window size for standard deviation. Default is 6.

    Returns:
        pd.DataFrame: DataFrame with a new column 'vol_{window}' containing volatility values.

    Raises:
        KeyError: If `ret_col` is not found in the DataFrame.
    """
    try:
        if ret_col not in table.columns:
            raise KeyError(f"Column '{ret_col}' not found in DataFrame")

        table[f"vol_{window}"] = table[ret_col].rolling(window).std()

    except Exception as e:
        print(f"[volatility] Error: {e}")
    return table


def trend_indicator(table, price_col="close", windows=[10, 20]):
    """
    Compute simple moving averages (SMA) and relative price-to-SMA ratios.

    Args:
        table (pd.DataFrame): Input DataFrame containing price data.
        price_col (str): Column name of the price series. Default is "close".
        windows (list[int]): List of SMA window sizes. Default is [10, 20].

    Returns:
        pd.DataFrame: DataFrame with new SMA columns ('sma_{window}') and
        ratio columns ('close_over_sma{window}').

    Raises:
        KeyError: If `price_col` is not found in the DataFrame.
    """
    try:
        if price_col not in table.columns:
            raise KeyError(f"Column '{price_col}' not found in DataFrame")

        for i in windows:
            sma = table[price_col].rolling(i).mean()
            table[f"sma_{i}"] = sma
            table[f"close_over_sma{i}"] = table[price_col] / sma

    except Exception as e:
        print(f"[trend_indicator] Error: {e}")
    return table


def bbands_feature(table, upper="upper_band", middle="middle_band", lower="lower_band", price_col="close"):
    """
    Add Bollinger Band features: %B and Bandwidth.

    Args:
        table (pd.DataFrame): Input DataFrame containing price and Bollinger Band data.
        upper (str): Column name for upper Bollinger Band. Default is "upper_band".
        middle (str): Column name for middle Bollinger Band. Default is "middle_band".
        lower (str): Column name for lower Bollinger Band. Default is "lower_band".
        price_col (str): Column name for the price series. Default is "close".

    Returns:
        pd.DataFrame: DataFrame with two new columns:
            - "bb_percentage": Position of price within the bands (0 to 1).
            - "bb_width": Relative width of the bands compared to the middle band.

    Raises:
        KeyError: If required Bollinger Band columns or `price_col` are missing.
    """
    try:
        missing_cols = [c for c in [upper, middle, lower, price_col] if c not in table.columns]
        if missing_cols:
            raise KeyError(f"Missing columns for Bollinger Bands: {missing_cols}")

        denominator = table[upper] - table[lower]
        if (denominator == 0).any():
            print("[bbands_feature] Warning: Zero denominator encountered")

        table["bb_percentage"] = (table[price_col] - table[lower]) / denominator
        table["bb_width"] = denominator / table[middle]

    except Exception as e:
        print(f"[bbands_feature] Error: {e}")
    return table


def check_momentum(table, price_col="close", momenta=[3, 6]):
    """
    Calculate momentum as the difference between current and lagged prices.

    Args:
        table (pd.DataFrame): Input DataFrame containing price data.
        price_col (str): Column name for the price series. Default is "close".
        momenta (list[int]): List of lags (in rows) to calculate momentum. Default is [3, 6].

    Returns:
        pd.DataFrame: DataFrame with new momentum columns ('momentum_{lag}').

    Raises:
        KeyError: If `price_col` is not found in the DataFrame.
    """
    try:
        if price_col not in table.columns:
            raise KeyError(f"Column '{price_col}' not found in DataFrame")

        for i in momenta:
            table[f"momentum_{i}"] = table[price_col] - table[price_col].shift(i)

    except Exception as e:
        print(f"[check_momentum] Error: {e}")
    return table


def add_lags(table, cols=("ret_1", "bb_percentage", "adx"), k=1):
    """
    Add lagged versions of selected columns.

    Args:
        table (pd.DataFrame): Input DataFrame containing feature columns.
        cols (tuple[str]): Columns to lag. Default is ("ret_1", "bb_percentage", "adx").
        k (int): Number of periods to lag. Default is 1.

    Returns:
        pd.DataFrame: DataFrame with new lagged columns named '{col}_lag{k}'.

    Notes:
        - Skips columns not present in the DataFrame, with a warning.
    """
    try:
        for i in cols:
            if i in table.columns:
                table[f"{i}_lag{k}"] = table[i].shift(k)
            else:
                print(f"[add_lags] Warning: Column '{i}' not found, skipping.")

    except Exception as e:
        print(f"[add_lags] Error: {e}")
    return table