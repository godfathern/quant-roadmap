import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("montreal_condo_hpi_sa_clean.csv")

print(len(df))
plt.figure()
plt.plot(df["Date"], df["Apartment_HPI_SA"])
plt.xlabel("Date")
plt.ylabel("HPI for condo (Seasonally adjusted)")
plt.title("Montreal Condo HPI")
plt.show()