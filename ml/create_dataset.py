import pandas as pd
from datetime import datetime

# Load cleaned data
customers = pd.read_csv("/Users/shreymittal/Desktop/retail_new/retail-data-warehouse/data/processed/cleaned_customers.csv")
transactions = pd.read_csv("/Users/shreymittal/Desktop/retail_new/retail-data-warehouse/data/processed/cleaned_transactions.csv")
products = pd.read_csv("/Users/shreymittal/Desktop/retail_new/retail-data-warehouse/data/processed/cleaned_products.csv")

# Convert dates
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
customers["join_date"] = pd.to_datetime(customers["join_date"])

# Merge price to calculate revenue
df = transactions.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

df["total_amount"] = df["quantity"] * df["price"]

# -----------------------------
# Customer Level Aggregation
# -----------------------------

today = df["transaction_date"].max()

customer_features = df.groupby("customer_id").agg(
    total_spend=("total_amount", "sum"),
    avg_order_value=("total_amount", "mean"),
    purchase_frequency=("transaction_id", "count"),
    last_purchase=("transaction_date", "max")
).reset_index()

# -----------------------------
# Recency (days since last purchase)
# -----------------------------

customer_features["recency"] = (
    today - customer_features["last_purchase"]
).dt.days

# -----------------------------
# Customer Age (days since join)
# -----------------------------

customer_features = customer_features.merge(
    customers[["customer_id", "join_date"]],
    on="customer_id",
    how="left"
)

customer_features["customer_age"] = (
    today - customer_features["join_date"]
).dt.days

# -----------------------------
# Churn Label
# -----------------------------
# If no purchase in last 90 days → churn = 1

customer_features["churn"] = customer_features["recency"].apply(
    lambda x: 1 if x > 90 else 0
)

# Drop unnecessary columns
customer_features.drop(columns=["last_purchase", "join_date"], inplace=True)

# -----------------------------
# Save dataset
# -----------------------------

import os
os.makedirs("../ml", exist_ok=True)

customer_features.to_csv("../ml/customer_dataset.csv", index=False)

print("✅ ML dataset created successfully!")
print(customer_features.head())