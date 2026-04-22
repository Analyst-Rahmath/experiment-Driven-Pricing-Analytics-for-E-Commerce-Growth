import pandas as pd

df = pd.read_csv("C:\\Users\\PC\\Desktop\\My Portfolio Projects\\Experiment-Driven Pricing Analytics for E-Commerce Growth\\data\\processed\\cleaned_data.csv")

print(df["Total_Amount"] == df["Unit_Price"] * df["Quantity"])

print(df.head())

print("Shape:", df.shape)
print("\nColumns:\n", df.columns)

print(df.dtypes)
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
print(df.describe())
print((df["Total_Amount"] == df["Unit_Price"] * df["Quantity"]).value_counts())

df["calculated_amount"] = (df["Unit_Price"] * df["Quantity"]).round(2)

print((df["Total_Amount"] == df["calculated_amount"]).value_counts())


