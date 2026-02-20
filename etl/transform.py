import pandas as pd

def calculate_revenue(transactions, products):
    merged = transactions.merge(
        products[["product_id", "price"]],
        on="product_id",
        how="left"
    )
    merged["total_amount"] = merged["quantity"] * merged["price"]
    return merged