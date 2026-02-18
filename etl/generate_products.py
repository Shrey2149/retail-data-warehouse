import pandas as pd
from faker import Faker
import random
import os

faker = Faker()

categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty", "Toys"]
products = []

for i in range(1,201):
    product = {"product_id" : i,
               "name" : faker.word().capitalize() + faker.word().capitalize(),
               "category" : random.choice(categories),
               "price" : round(random.uniform(5.0, 500.0),2)}
    products.append(product)

df = pd.DataFrame(products)

os.makedirs("../data/raw", exist_ok=True)

df.to_csv("../data/raw/products.csv",index = False)
print("200 products generated successfully")

    