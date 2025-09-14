from dataConversion import merge_tables, build_features, binary_convert
from client import Client
from predictor import Predictor

def run(ticker, interval):  
    client = Client.configure()

    #retrieve data from client 
    adx = client.get_adx(ticker, interval)
    b_bands = client.get_bbands(ticker, interval)
    t_series = client.get_tSeries(ticker, interval)

    #features, data prep
    df = merge_tables(adx, b_bands, t_series)
    df = build_features(df)
    df = binary_convert(df)
   
    #train and predict
    #exclude raw data to access only feature columns
    exclude = ["open", "high", "low", "close", "volume", "upper_band", "middle_band", "lower_band", "target"]
    feature_cols = [col for col in df.columns if col not in exclude]

    predictor = Predictor(feature_cols)
    predictor.train(df)
    predictor.predict(df)
   

if __name__ == "__main__":
    #Selection
    print("Options: 1day, 1week, 1month")
    interval = input("Choose an interval to train the model with: ")
    ticker = input("Choose a stock ticker (e.g., AAPL, MSFT): ")

    run(ticker, interval)
