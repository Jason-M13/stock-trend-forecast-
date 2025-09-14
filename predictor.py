import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

class Predictor:
    def __init__(self, feature_cols):
        self.feature_cols = feature_cols
        self.model = LogisticRegression(max_iter=1000)

    def train(self,df):
        x = df[self.feature_cols].copy()
        y = df["target"].copy()

        x = x.replace([np.inf, -np.inf],np.nan).dropna()
        y = y.loc[x.index]

        x_train, x_test, y_train, y_test = train_test_split(x,y, shuffle = False, test_size = 0.2)

        self.model.fit(x_train, y_train)
        acc = self.model.score(x_test, y_test)
        self.x_test, self.y_test = x_test, y_test

        print(f"Test Accuracy: {acc}")

        return x,y
    
    def predict(self, df):
        latest = df[self.feature_cols].iloc[[-1]]
        probablity = self.model.predict_proba(latest)[0]
        
        prediction = int(probablity[1] >= 0.5)
        if prediction == 1:
            direction = "Up"
        else:
            direction = "Down"
        
        confidence = max(probablity)

        print("\nLatest Prediction:")
        print(f"Direction: {direction}")
        print(f"Confidence Rate: {confidence:.2%}")

        return direction, confidence 
    