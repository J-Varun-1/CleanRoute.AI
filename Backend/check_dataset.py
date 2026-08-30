import pandas as pd


df = pd.read_csv(
    "data/indian_waste_data_v2.csv"
)


print("\n==============================")
print("COLUMNS")
print("==============================")

print(
    df.columns.tolist()
)


print("\n==============================")
print("SHAPE")
print("==============================")

print(
    df.shape
)


print("\n==============================")
print("DATE RANGE")
print("==============================")

df["date"] = pd.to_datetime(
    df["date"]
)

print(
    df["date"].min()
)

print(
    df["date"].max()
)


print("\n==============================")
print("BINS")
print("==============================")

print(
    df["bin_id"].nunique()
)


print("\n==============================")
print("ROWS PER BIN")
print("==============================")

print(
    df.groupby("bin_id")
      .size()
      .describe()
)


print("\n==============================")
print("MISSING VALUES")
print("==============================")

print(
    df.isna().sum()
)