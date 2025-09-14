import matplotlib.pyplot as plt
import pandas as pd

class Visualizer:
    def __init__(self, X_test, y_test, proba_up):
        """
        X_test: DataFrame with DateTimeIndex (features for test set)
        y_test: Series of actual outcomes (0=Down, 1=Up)
        proba_up: numpy array of predicted probabilities for Up
        """
        self.X_test = X_test
        self.y_test = y_test
        self.proba_up = proba_up

        # tidy DataFrame for plotting
        self.plot_df = pd.DataFrame({
            "actual": self.y_test.values,
            "p_up": self.proba_up
        }, index=self.X_test.index)
        self.plot_df["pred"] = (self.plot_df["p_up"] >= 0.5).astype(int)
        self.plot_df["correct"] = (self.plot_df["pred"] == self.plot_df["actual"])

    def plot_backtest(self):
        plt.figure(figsize=(10, 5))

        # 1. Confidence line
        plt.plot(self.plot_df.index, self.plot_df["p_up"], label="Model Confidence")

        # 2. Correct vs wrong markers
        correct_pts = self.plot_df[self.plot_df["correct"]]
        wrong_pts = self.plot_df[~self.plot_df["correct"]]
        plt.scatter(correct_pts.index, correct_pts["p_up"], marker="o", label="Correct", zorder=3)
        plt.scatter(wrong_pts.index,   wrong_pts["p_up"],   marker="x", label="Wrong",   zorder=3)

        # 3. Threshold
        plt.axhline(0.5, linestyle="--", linewidth=1, label="Decision threshold (0.5)")

        plt.title("Probability of Up")
        plt.ylabel("Probability")
        plt.xlabel("Date")
        plt.ylim(-0.05, 1.05)
        plt.legend()
        plt.tight_layout()
        plt.show()
