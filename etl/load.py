import pandas as pd
from config import get_engine
from transform import calculate_revenue

engine = get_engine()

products = pd.read_csv("data/processed/cleaned_products.csv")
customers = pd.read_csv("data/processed/cleaned_customers.csv")
transactions = pd.read_csv("data/processed/cleaned_transactions.csv")

# Load dimensions
products.to_sql("dim_product", engine, if_exists="append", index=False)
customers.to_sql("dim_customer", engine, if_exists="append", index=False)

# Transform
fact_df = calculate_revenue(transactions, products)

fact_df.to_sql("fact_sales", engine, if_exists="append", index=False)

print("ETL pipeline completed successfully.")