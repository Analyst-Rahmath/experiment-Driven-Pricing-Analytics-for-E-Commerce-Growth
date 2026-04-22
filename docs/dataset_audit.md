# 📊 Dataset Audit Summary

## Basic Info

* Total Records: 1200
* Total Columns: 7
* Dataset Type: E-commerce transactions (2025)

## Columns Identified

* Order_ID: Unique identifier for each order
* Country: Customer location
* Category: Product category
* Unit_Price: Price per unit
* Quantity: Number of units purchased
* Order_Date: Date of transaction
* Total_Amount: Total revenue per order

## Data Quality Check

* Missing Values: None
* Duplicates: None
* Data Types Issue: Order_Date is in string format

## Observations

* Dataset is clean and well-structured
* Contains diverse pricing and quantity distribution
* Suitable for A/B testing simulation
* No experiment-related columns present
## Revenue Validation Check

* Verified that Total_Amount equals Unit_Price × Quantity
* Initial mismatches (170 rows) observed due to floating-point precision
* After rounding to 2 decimal places, all 1200 rows matched
* Dataset confirmed to be fully consistent and reliable

## Potential Issues

* Order_Date needs conversion to datetime

## Next Step

Proceed to data cleaning and feature engineering
