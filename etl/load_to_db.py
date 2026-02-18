import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# Database Connection
# -----------------------------
username = "postgres"
password = "shreythegreat"
host = "localhost"
port = "5432"
database = "retail_dw"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

# -----------------------------
# Load Cleaned Data
# -----------------------------
products = pd.read_csv("../data/processed/cleaned_products.csv")
customers = pd.read_csv("../data/processed/cleaned_customers.csv")
transactions = pd.read_csv("../data/processed/cleaned_transactions.csv")

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

fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False)
print("✅ fact_sales loaded")

print("🎯 Data successfully loaded into warehouse!")