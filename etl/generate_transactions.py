import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

transactions = []

for i in range(1, 10001):
    transaction = {
        "transaction_id": i,
        "product_id": random.randint(1, 200),
        "customer_id": random.randint(1, 1000),
        "quantity": random.randint(1, 5),
        "transaction_date": fake.date_between(start_date="-2y", end_date="today")
    }
    transactions.append(transaction)

df = pd.DataFrame(transactions)

os.makedirs("../data/raw", exist_ok=True)
df.to_csv("../data/raw/transactions.csv", index=False)

print("✅ 10,000 transactions generated successfully!")