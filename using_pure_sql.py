import sqlite3
import csv

# Connect to the SQLite database
connection = sqlite3.connect('PROMOSALES.db')
cursor = connection.cursor()

# SQL query to extract data
query = """
    SELECT C.customer_id, C.age, I.item_name, IFNULL(SUM(S.Quantity), 0) AS Quantity
    FROM Orders O
    INNER JOIN Sales S ON s.sales_id = O.sales_id
    INNER JOIN Customer C ON s.customer_id=C.customer_id
    INNER JOIN Items i ON O.item_id = i.item_id
    WHERE C.age >= 18 AND C.age <= 35 
    AND O.quantity IS NOT NULL
    GROUP BY c.customer_id, i.item_name
    having SUM(O.Quantity) > 0 
"""

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Close the database connection
connection.close()

# Write the results to a CSV file
with open('/Users/dwijs/sqlite3/output_sql.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=';')
    csv_writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])
    
    # Write rows from the results list
    for row in results:
        csv_writer.writerow([row['CustomerID'], row['Age'], row['ItemName'], row['Quantity']])
