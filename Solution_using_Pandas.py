import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')

# Load necessary tables into Pandas DataFrames
customers_df = pd.read_sql_query("SELECT customer_id, age FROM Customer", conn)
sales_df = pd.read_sql_query("SELECT sales_id, customer_id FROM Sales", conn)
orders_df = pd.read_sql_query("SELECT sales_id, item_id, quantity FROM Orders", conn)
items_df = pd.read_sql_query("SELECT item_id, item_name FROM Items", conn)

# Merge DataFrames to get a combined dataset
combined_df = pd.merge(customers_df, sales_df, on='customer_id')
combined_df = pd.merge(combined_df, orders_df, on='sales_id')
combined_df = pd.merge(combined_df, items_df, on='item_id')

# Filter data based on age and non-null quantity
filtered_df = combined_df[(combined_df['age'] >= 18) & (combined_df['age'] <= 35) & (combined_df['quantity'].notnull())]

# Group by customer_id and item_name, summing up quantities
result_df = filtered_df.groupby(['customer_id', 'item_name']).agg({'quantity': 'sum'}).reset_index()
result_df.rename(columns={'quantity': 'Quantity'}, inplace=True)

# Filter out rows with Quantity <= 0
result_df = result_df[result_df['Quantity'] > 0]

# Close the database connection
conn.close()

# Write the DataFrame to a CSV file
result_df.to_csv('output_pandas.csv', sep=';', index=False)
