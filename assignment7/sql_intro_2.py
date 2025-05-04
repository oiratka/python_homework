
import sqlite3
import pandas as pd

#Find out how many times each product was ordered, and what was the total price paid by product.

with sqlite3.connect("../db/lesson.db") as conn:
    df = pd.read_sql_query("""
        SELECT
            line_items.line_item_id,
            line_items.quantity,
            line_items.product_id,
            products.product_name,
            products.price
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
        """, conn)
    print(df.head(5))

    #add a column to DF
    df['total'] = df['quantity'] * df['price']
    print(df.head(5))
    summary = df.groupby('product_id').agg({
        "line_item_id": "count",
        "total": "sum",
        "product_name": "first"
    })
    print(summary.head(5))
    
    df = df.sort_values(by='product_name')
    print(df)

    summary.to_csv('order_summary.csv')

