# db_builder.py
import pandas as pd
import sqlite3

# Load Excel files
ad_sales = pd.read_excel("data/Product-Level Ad Sales and Metrics.xlsx")
total_sales = pd.read_excel("data/Product-Level Total Sales and Metrics.xlsx")
eligibility = pd.read_excel("data/Product-Level Eligibility Table.xlsx")

# Create DB
conn = sqlite3.connect("sales.db")

# Store tables
ad_sales.to_sql("product_ad_sales", conn, if_exists="replace", index=False)
total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)
eligibility.to_sql("eligibility_table", conn, if_exists="replace", index=False)

print("Database created as 'sales.db'")
