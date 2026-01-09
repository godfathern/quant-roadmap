import pandas as pd
import numpy as np
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FILEPATH = BASE_DIR / "Seasonally Adjusted (M).xlsx"
TARGET_COL = "Apartment_HPI_SA"   

df = pd.read_excel(FILEPATH)

date_col = df.columns[0]
series = df[["Date", TARGET_COL]].reset_index(drop=True)


LOOKBACK = 24   # look at past 24 months
HORIZON = 12    # predict next 12 months

y = series[TARGET_COL].values.astype(np.float32)

print("total row cac", len(y))

def make_windows(y, lookback, horizon):
    X, Y = [], []
    for i in range(lookback, len(y) - horizon + 1):
        X.append(y[i - lookback:i])
        Y.append(y[i:i + horizon])
    return np.array(X, dtype=np.float32), np.array(Y, dtype=np.float32)

X, Y = make_windows(y, LOOKBACK, HORIZON)

print("Loaded rows:", len(series))
print("X shape (samples, lookback):", X.shape)
print("Y shape (samples, horizon):", Y.shape)

split = int(len(X) * 0.8)
X_train, Y_train = X[:split], Y[:split]
X_test,  Y_test  = X[split:], Y[split:]

print("Train samples:", X_train.shape[0], "Test samples:", X_test.shape[0])

# Save cleaned dataset for reproducibility
out_csv = Path("montreal_condo_hpi_sa_clean.csv")
series.to_csv(out_csv, index=False)
print("Saved cleaned series to:", out_csv.resolve())
