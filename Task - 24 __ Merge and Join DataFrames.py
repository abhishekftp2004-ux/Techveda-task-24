"""
TASK 24: MERGE AND JOIN DATAFRAMES
Track: Data Science
Libraries: Python, Pandas
Run from the folder containing customers.csv, orders.csv, and payments.csv.
"""

import pandas as pd

# TOPIC 1 — Load and inspect datasets
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
payments = pd.read_csv("payments.csv")

print("\nCUSTOMERS")
print(customers.to_string(index=False))
print("\nORDERS")
print(orders.to_string(index=False))
print("\nPAYMENTS")
print(payments.to_string(index=False))

print("\nSHAPES:", customers.shape, orders.shape, payments.shape)
print("\nCUSTOMER DATA TYPES")
print(customers.dtypes)

# TOPIC 2 — INNER JOIN: only keys present in both tables
inner_join = customers.merge(orders, on="CustomerID", how="inner")
print("\nINNER JOIN")
print(inner_join.to_string(index=False))

# TOPIC 3 — LEFT JOIN: preserve every customer
left_join = customers.merge(orders, on="CustomerID", how="left", indicator=True)
print("\nLEFT JOIN (with merge indicator)")
print(left_join.to_string(index=False))

# TOPIC 4 — RIGHT JOIN: preserve every order
right_join = customers.merge(orders, on="CustomerID", how="right", indicator=True)
print("\nRIGHT JOIN (with merge indicator)")
print(right_join.to_string(index=False))

# TOPIC 5 — OUTER JOIN: preserve all customers and orders
outer_join = customers.merge(orders, on="CustomerID", how="outer", indicator=True)
print("\nOUTER JOIN (with merge indicator)")
print(outer_join.to_string(index=False))

# TOPIC 6 — Merge on a different key: orders + payment details
orders_with_payments = orders.merge(
    payments, on="OrderID", how="left", indicator="PaymentMatch"
)
print("\nORDERS WITH PAYMENT DETAILS")
print(orders_with_payments.to_string(index=False))

# TOPIC 7 — Multi-table merge: final combined dataset
final_dataset = (
    customers
    .merge(orders, on="CustomerID", how="outer")
    .merge(payments, on="OrderID", how="left")
)
print("\nFINAL COMBINED DATASET")
print(final_dataset.to_string(index=False))

# TOPIC 8 — Identify unmatched records
customers_without_orders = left_join[left_join["_merge"] == "left_only"]
orders_without_customer = right_join[right_join["_merge"] == "right_only"]
orders_without_payment = orders_with_payments[
    orders_with_payments["PaymentMatch"] == "left_only"
]
print("\nCUSTOMERS WITHOUT ORDERS")
print(customers_without_orders[["CustomerID", "CustomerName", "City"]].to_string(index=False))
print("\nORDERS WITHOUT MATCHING CUSTOMER")
print(orders_without_customer[["OrderID", "CustomerID", "Amount"]].to_string(index=False))
print("\nORDERS WITHOUT MATCHING PAYMENT RECORD")
print(orders_without_payment[["OrderID", "CustomerID", "Amount"]].to_string(index=False))

# TOPIC 9 — Duplicate keys and relationship cardinality
print("\nCUSTOMER ID UNIQUE IN CUSTOMERS:", customers["CustomerID"].is_unique)
print("CUSTOMER ID UNIQUE IN ORDERS:", orders["CustomerID"].is_unique)
order_counts = orders.groupby("CustomerID", as_index=False).size().rename(columns={"size": "OrderCount"})
print("\nORDER COUNT BY CUSTOMER ID")
print(order_counts.to_string(index=False))

# TOPIC 10 — Validation: enforce expected relationship where appropriate
# Each customer should be unique in customers; validate='one_to_many' checks
# left keys are unique and right keys may repeat.
validated_merge = customers.merge(
    orders, on="CustomerID", how="left", validate="one_to_many"
)
print("\nVALIDATED LEFT MERGE ROW COUNT:", len(validated_merge))

# TOPIC 11 — Alternative key names (example only)
# If customers used CustomerID but orders used ClientID:
# customers.merge(orders.rename(columns={"CustomerID": "ClientID"}),
#                 left_on="CustomerID", right_on="ClientID", how="left")

# TOPIC 12 — Save all outputs
inner_join.to_csv("inner_join.csv", index=False)
left_join.to_csv("left_join.csv", index=False)
right_join.to_csv("right_join.csv", index=False)
outer_join.to_csv("outer_join.csv", index=False)
orders_with_payments.to_csv("orders_with_payments.csv", index=False)
final_dataset.to_csv("final_combined_dataset.csv", index=False)
customers_without_orders.to_csv("customers_without_orders.csv", index=False)
orders_without_customer.to_csv("orders_without_customer.csv", index=False)
orders_without_payment.to_csv("orders_without_payment.csv", index=False)

print("\nAll join results and the final combined dataset have been saved as CSV files.")
