"""
CodeOrbit Tech Data Analyst Internship — Sales Data Analysis
Uses a sample dataset included in this project. Replace the sample CSV with your assigned data if required.
"""
import pandas as pd

# The raw dataset is included in CodeOrbit_Sales_Analysis.xlsx (Raw_Data sheet).
# Export Raw_Data as raw_sales.csv before running this script, or change the input path below.
INPUT_FILE = "raw_sales.csv"

df = pd.read_csv(INPUT_FILE)
print("Raw rows:", len(df))

# Standardize text fields
for col in ["Order_ID", "Region", "Category", "Product", "Channel"]:
    df[col] = df[col].astype("string").str.strip()

for col in ["Region", "Category", "Product", "Channel"]:
    df[col] = df[col].str.title()

# Convert data types
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

# Documented sample assumptions for missing values
df["Product"] = df["Product"].fillna("Unknown")
df["Quantity"] = df["Quantity"].fillna(1)

# Remove duplicate business records
df = df.drop_duplicates(
    subset=["Order_Date", "Region", "Category", "Product", "Unit_Price", "Quantity", "Channel"],
    keep="first"
)

df["Sales"] = df["Unit_Price"] * df["Quantity"]
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

total_sales = df["Sales"].sum()
order_count = df["Order_ID"].nunique()
average_order_value = total_sales / order_count if order_count else 0

print(f"Total sales: ₹{total_sales:,.2f}")
print(f"Number of orders: {order_count}")
print(f"Average order value: ₹{average_order_value:,.2f}")
print("\\nSales by product:")
print(df.groupby("Product")["Sales"].sum().sort_values(ascending=False))
print("\\nSales by category:")
print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False))
print("\\nSales by region:")
print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False))
print("\\nMonthly sales:")
print(df.groupby("Month")["Sales"].sum())
df.to_csv("cleaned_sales.csv", index=False)
print("\\nSaved cleaned data to cleaned_sales.csv")
