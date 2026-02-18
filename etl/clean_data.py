import os
import pandas as pd

products = pd.read_csv("../data/raw/products.csv")

products.dropna(inplace=True)
products.drop_duplicates(inplace = True)

products.to_csv("../data/processed/cleaned_products.csv",index = False)
print("Cleaned Products")

customers = pd.read_csv("../data/raw/customers.csv")

customers.dropna(inplace=True)
customers.drop_duplicates(inplace = True)
if "join_date" in customers.columns:
    customers["join_date"] = pd.to_datetime(customers["join_date"])
customers.to_csv("../data/processed/cleaned_customers.csv",index = False)
print("Cleaned Customers")

tran = pd.read_csv("../data/raw/transactions.csv")

tran.dropna(inplace=True)
tran.drop_duplicates(inplace = True)
tran["transaction_date"] = pd.to_datetime(tran["transaction_date"])
tran.to_csv("../data/processed/cleaned_transactions.csv",index = False)
print("Cleaned Transactions")

print("All data cleaned successfully!")