import sqlite3


try:
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
    
        cursor.execute("""
        SELECT orders.order_id, SUM (products.price * line_items.quantity)
        AS total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.order_id
        ORDER BY orders.order_id
        LIMIT 5
        """)

        result = cursor.fetchall()
        for order_id, total_price in result:
           print(f"Order ID: {order_id}, Total price: ${total_price:.2f}")

# Adding new orders        
        cursor.execute("""
        SELECT customers.customer_name, AVG(order_totals.total_price) AS average_total_price
        FROM Customers
        LEFT JOIN(
                SELECT orders.customer_id AS customer_id_b, SUM(products.price * line_items.quantity)
                AS total_price
                FROM orders
                JOIN line_items ON orders.order_id = line_items.order_id
                JOIN products ON line_items.product_id = products.product_id
                GROUP BY orders.order_id
        ) AS order_totals
        ON customers.customer_id = order_totals.customer_id_b
        GROUP BY customers.customer_id
        LIMIT 5
        """)

        avg_result = cursor.fetchall()
        for customer_name, avg_price in avg_result:
            if avg_price is None:
                 avg_price = 0 
            print(f"Customer Name: {customer_name}, Average order price: ${avg_price:.2f}")
        
        cursor.execute("""
        SELECT customers.customer_id
        FROM Customers
        WHERE customer_name = "Perez and Sons";
        """)
        customer_id = cursor.fetchone()[0]

        cursor.execute("""
        SELECT employees.employee_id
        FROM Employees
        WHERE first_name = "Miranda" and last_name = "Harris";
        """)
        employee_id = cursor.fetchone()[0]

        cursor.execute("""
        SELECT products.product_id, price
        FROM Products
        ORDER BY price ASC
        LIMIT 5
        """)
        product_rows = cursor.fetchall()

        cursor.execute("""
        INSERT INTO Orders (customer_id, employee_id)
        VALUES (?, ?);
        """, (customer_id, employee_id)) 
        order_id = cursor.lastrowid

        for row in product_rows:
            product_id = row[0]
            quantity = 10
            cursor.execute("""
               INSERT INTO Line_items (product_id,order_id, quantity)
               VALUES (?,?,?)
            """, (product_id, order_id, quantity))

        cursor.execute("""
        SELECT line_items.line_item_id, quantity, products.product_name
        From Line_items
        JOIN Products ON line_items.product_id = products.product_id
        WHERE line_items.order_id = ?
        """, (order_id,))
        final_results = cursor.fetchall()
        print("\nLine_items for new order:")
        for line_item_id, quantity, product_name in final_results:
            print(f"Line item ID: {line_item_id}, Product: {product_name}, Quantity: {quantity}")
        
        cursor.execute("""
        DELETE FROM Line_items
        Where order_id = (SELECT last_insert_rowid())
        """)
        cursor.execute("""
        DELETE FROM Orders
        WHERE order_id = (SELECT last_insert_rowid())
        """)
        print("\n Recors deleted successfully")

#HAVING
        cursor.execute("""
        SELECT e.employee_id, e.first_name, e.last_name, COUNT (order_id)as order_count
        FROM Employees AS e
        JOIN Orders AS o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
        """)
        results = cursor.fetchall()
        for employee_id, first_name, last_name, order_count in results:
            print(f"Employee ID: {employee_id}, First Name: {first_name}, Last name {last_name}, Orders: {order_count}")

except sqlite3.Error as e:
    print('Database error:', e)







