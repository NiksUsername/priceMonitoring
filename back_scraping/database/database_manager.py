import sqlite3


def fetch_data_as_dict(site_name):
    data_dict = {}

    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        # Fetch all rows from the data_table
        cursor.execute(f"SELECT * FROM {site_name}")
        rows = cursor.fetchall()

        # Process each row and populate the data_dict
        for row in rows:
            row_dict = {
                "name": row[0],
                "price": row[1],
                "link": row[2],
                "old_price": row[3]
            }
            # Use the 'link' value as the key in the data_dict
            data_dict[row[2]] = row_dict

    finally:
        # Close the database connection
        cursor.close()
        conn.close()

    return data_dict


def write_data_to_db(data_dict, site_name):
    # Connect to the SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        # Iterate over each item in the data_dict
        for link, product_data in data_dict.items():
            name = product_data.get('name', '')
            price = product_data.get('price', 0.0)
            old_price = product_data.get('old_price', price)

            # Execute UPSERT (INSERT or UPDATE) using REPLACE in SQLite
            cursor.execute(f"REPLACE INTO {site_name} (name, price, link, old_price) VALUES (?, ?, ?, ?)",
                           (name, price, link, old_price))

        # Commit the transaction
        conn.commit()

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
