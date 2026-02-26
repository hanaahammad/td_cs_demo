from sklearn.datasets import fetch_openml
import pandas as pd

print("Downloading Online Retail dataset...")

# OpenML hosts a stable mirror
data = fetch_openml(

    name="Online Retail",

    version=1,

    as_frame=True

)

df = data.frame

print("Rows:", len(df))

df.to_csv(

    "online_retail.csv",

    index=False

)

print("Saved as online_retail.csv")
