import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("montreal_condo_hpi_sa_clean.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

y = df["Apartment_HPI_SA"].astype(float)

# ---- Train/Test split (time-based) ----
split = int(len(df) * 0.8)
train = df.iloc[:split].copy()
test  = df.iloc[split:].copy()

# ---- Naive 1-step forecast: y_hat(t) = y(t-1) ----
prev_values = pd.concat([train["Apartment_HPI_SA"].tail(1), test["Apartment_HPI_SA"].iloc[:-1]])
test["y_pred_naive"] = prev_values.values

# ---- Metrics ----
y_true = test["Apartment_HPI_SA"].values
y_pred = test["y_pred_naive"].values

mae = np.mean(np.abs(y_true - y_pred))
rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Direction accuracy:
# Compare changes: (y_t - y_{t-1}) sign
y_true_change = np.sign(y_true[1:] - y_true[:-1])
y_pred_change = np.sign(y_pred[1:] - y_true[:-1])  # predicted vs last actual
direction_acc = np.mean(y_true_change == y_pred_change) * 100

print("Naive baseline (1-step ahead) on TEST")
print(f"Test months: {len(test)}")
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAPE: {mape:.4f}%")
print(f"Direction accuracy: {direction_acc:.2f}%")

# Show a few rows to sanity-check predictions
print("\nSample predictions:")
print(test[["Date", "Apartment_HPI_SA", "y_pred_naive"]].head(10))
