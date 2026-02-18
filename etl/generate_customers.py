import os 
from faker import Faker
import random
import pandas as pd

fake = Faker()
segments = ["Regular", "Premium","VIP", "Corporate"]
customers = []

for i in range(1,1001):
    customer = {
        "customer_id" : i,
        "name" : fake.name(),
        "city" : fake.city(),
        "state" : fake.state(),
        "join_date" : fake.date_between(start_date = "-5y", end_date="today"),
        "segment" : random.choice(segments)
    }
    customers.append(customer)
df = pd.DataFrame(customers)
os.makedirs("../data/raw",exist_ok=True)
df.to_csv("../data/raw/customers.csv",index = False)

print("1000 customers are generated")
