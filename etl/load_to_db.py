import pandas as pd
import os
from sqlalchemy import create_engine, text

# -----------------------------
# Database Connection (Render)
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not set. Please export it first.")

engine = create_engine(DATABASE_URL)

# -----------------------------
# Reset Tables (Avoid duplicates)
# -----------------------------
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE fact_sales CASCADE;"))
    conn.execute(text("TRUNCATE TABLE dim_customer CASCADE;"))
    conn.execute(text("TRUNCATE TABLE dim_product CASCADE;"))
    conn.commit()

print("✅ Tables truncated")

# -----------------------------
# Load Cleaned Data
# -----------------------------
products = pd.read_csv("data/processed/cleaned_products.csv")
customers = pd.read_csv("data/processed/cleaned_customers.csv")
transactions = pd.read_csv("data/processed/cleaned_transactions.csv")

# Ensure date format
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

# -----------------------------
# Insert Dimension Tables
# -----------------------------
products.to_sql("dim_product", engine, if_exists="append", index=False)
print("✅ dim_product loaded")

customers.to_sql("dim_customer", engine, if_exists="append", index=False)
print("✅ dim_customer loaded")

# -----------------------------
# Prepare Fact Table
# -----------------------------
merged = transactions.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

merged["total_amount"] = merged["quantity"] * merged["price"]

fact_sales = merged[[
    "transaction_id",
    "customer_id",
    "product_id",
    "quantity",
    "total_amount",
    "transaction_date"
]]

# -----------------------------
# Insert Fact Table
# -----------------------------
fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False)
print("✅ fact_sales loaded")

print("🎯 Data successfully loaded into warehouse!")