import pandas as pd
import numpy as np

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("montreal_condo_hpi_sa_clean.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

y = df["Apartment_HPI_SA"].astype(float)

# -----------------------------
# Train / Test split (time-based)
# -----------------------------
split = int(len(df) * 0.8)
train = df.iloc[:split].copy()
test  = df.iloc[split:].copy()

# -----------------------------
# Rolling mean predictor
# -----------------------------
def rolling_mean_predict(train_series, test_series, k):
    """
    1-step ahead rolling mean predictor.
    """
    history = list(train_series.values)
    preds = []

    for actual in test_series.values:
        pred = np.mean(history[-k:])   # rolling mean of last k months
        preds.append(pred)
        history.append(actual)         # update history with real value

    return np.array(preds)

# -----------------------------
# Evaluate for different K
# -----------------------------
for k in [3, 6, 12]:
    y_pred = rolling_mean_predict(
        train["Apartment_HPI_SA"],
        test["Apartment_HPI_SA"],
        k
    )

    y_true = test["Apartment_HPI_SA"].values

    mae  = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    print(f"\nRolling Mean Baseline (K={k})")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAPE: {mape:.4f}%")
