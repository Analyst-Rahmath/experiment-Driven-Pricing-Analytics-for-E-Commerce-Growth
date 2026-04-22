import pandas as pd

df = pd.read_csv("C:\\Users\\PC\\Desktop\\My Portfolio Projects\\Experiment-Driven Pricing Analytics for E-Commerce Growth\\data\\processed\\cleaned_data.csv")

#step1: Convert "Order_Date" to datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format='mixed', dayfirst=True)
print(df["Order_Date"].dtype)
print(df["Order_Date"].isnull().sum())

#step 2: Extract month, quarter, and year from "Order_Date" and create new columns
df["Month"] = df["Order_Date"].dt.month.astype(int)
df["Quarter"] = df["Order_Date"].dt.quarter.astype(int)
df["Year"] = df["Order_Date"].dt.year.astype(int)

#step 3: Create a new column "Calculated_Amount" by multiplying "Unit_Price" and "Quantity"
df["calculated_amount"] = (df["Unit_Price"] * df["Quantity"]).round(2)

#step 4: Standardize column names to lowercase
df.columns = df.columns.str.lower()

df.drop(columns=["calculated_amount"], inplace=True, errors='ignore')
#step 5: Check the data types of the columns after transformations
print(df.dtypes)

#step 6: Save the cleaned and transformed data to a new CSV file
df.to_csv("C:\\Users\\PC\\Desktop\\My Portfolio Projects\\Experiment-Driven Pricing Analytics for E-Commerce Growth\\data\\processed\\cleaned_data_final.csv", index=False)

