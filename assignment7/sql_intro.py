import sqlite3

# Task 3: Populate Tables

def add_publishers(cursor, name):
    try:
        cursor.execute("INSERT INTO Publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database")

def add_magazines(cursor, magazine_name, publisher_name):
    try:
        cursor.execute("SELECT publisher_id FROM Publishers WHERE name = ?", (publisher_name,))
        result = cursor.fetchone()
        if result:
            publisher_id = result[0]
            cursor.execute("INSERT INTO Magazines (magazine_name, publisher_id) VALUES (?, ?)", (magazine_name, publisher_id))
        else:
            print(f"Publisher '{publisher_name}' not found. Cannot add magazine '{magazine_name}'.")
    except sqlite3.IntegrityError:
        print(f"{magazine_name} is already in the database")

def add_subscribers(cursor, subscriber_name, address):
    try:
        cursor.execute("SELECT * FROM Subscribers WHERE subscriber_name = ? AND address = ?", (subscriber_name, address))
        results = cursor.fetchall()
        if not results:
            cursor.execute("INSERT INTO Subscribers (subscriber_name, address) VALUES (?, ?)", (subscriber_name, address))
    except sqlite3.IntegrityError:
        print(f"{subscriber_name} at {address} is already in the database")

def add_subscriptions(cursor, subscriber_name, magazine_name, expiration_date):
    cursor.execute("SELECT subscriber_id FROM Subscribers WHERE subscriber_name = ?", (subscriber_name,))
    result = cursor.fetchall()
    if result:
        subscriber_id = result[0][0]
    else:
        print(f"There was no subscriber named {subscriber_name}")
        return
    cursor.execute("SELECT magazine_id FROM Magazines WHERE magazine_name = ?", (magazine_name,))
    result = cursor.fetchall()
    if result:
        magazine_id = result[0][0]
    else:
        print(f"There was no magazine named {magazine_name}")
        return
    
    try:
        cursor.execute("INSERT INTO Subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)", (subscriber_id, magazine_id, expiration_date))
    except sqlite3.IntegrityError:
        print(f"Subscription already exists or cannot insert")

with sqlite3.connect("../db/magazines.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Subscriptions")
    cursor.execute("DROP TABLE IF EXISTS Magazines")
    cursor.execute("DROP TABLE IF EXISTS Subscribers")
    cursor.execute("DROP TABLE IF EXISTS Publishers")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Publishers(
            publisher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Magazines(
            magazine_id INTEGER PRIMARY KEY,
            magazine_name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subscribers(
            subscriber_id INTEGER PRIMARY KEY,
            subscriber_name TEXT NOT NULL,
            address TEXT,
            UNIQUE(subscriber_name, address)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subscriptions(
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER,
            magazine_id INTEGER,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES Subscribers (subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES Magazines (magazine_id),
            UNIQUE(subscriber_id, magazine_id)
    )
    """)
    print("Tables created successfully")

    add_publishers(cursor, "Conde Nast")
    add_publishers(cursor, "Hearst Communications")
    add_publishers(cursor, "Meredith Corp")
    
    add_magazines(cursor, "Vogue", "Conde Nast")
    add_magazines(cursor, "GQ", "Conde Nast")
    add_magazines(cursor, "Elle", "Hearst Communications")
    add_magazines(cursor, "Allrecipes", "Meredith Corp")
    
    add_subscribers(cursor, "Bob Dylan", "R88 Sunset Blvd, Los Angeles, CA")
    add_subscribers(cursor, "Priya Kapoor", "12 Lotus Ave, Austin, TX")
    add_subscribers(cursor, "Maria Silva", "910 Ocean Drive, Miami, FL")
    add_subscribers(cursor, "Jamal Rodriguez", "910 Ocean Drive, Miami, FL")
    add_subscribers(cursor, "Alice Bennett", "942 Maple Street, Springfield, IL")
    
    add_subscriptions(cursor, "Bob Dylan", "GQ", "10/01/2025")
    add_subscriptions(cursor, "Priya Kapoor", "Elle", "08/01/2025")
    add_subscriptions(cursor, "Maria Silva", "Allrecipes", "12/01/2025")
    add_subscriptions(cursor, "Maria Silva", "Elle", "12/01/2025")
    add_subscriptions(cursor, "Jamal Rodriguez", "GQ", "12/01/2025")
    add_subscriptions(cursor, "Alice Bennett", "Vogue", "12/01/2025")
    add_subscriptions(cursor, "Alice Bennett", "Vogue", "12/01/2025")
    add_subscriptions(cursor, "Alice Bennett", "Elle", "07/01/2025")

    # Remove duplicate subscriptions
    cursor.execute("""
        DELETE FROM Subscriptions
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM Subscriptions
            GROUP BY subscriber_id, magazine_id
        )
    """)

    # Display Subscribers
    cursor.execute("""
    SELECT * FROM Subscribers
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Display Magazines
    cursor.execute("""
    SELECT * FROM Magazines
    ORDER BY magazine_name
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Display Magazines from a specific Publisher
    cursor.execute("""
    SELECT Magazines.magazine_name
    FROM Magazines
    JOIN Publishers ON Magazines.publisher_id = Publishers.publisher_id
    WHERE Publishers.name = ?
    """, ("Hearst Communications",))





