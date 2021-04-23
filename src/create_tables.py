import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# to create user table
create_users_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR, password VARCHAR)"

cursor.execute(create_users_query)


#to create items table
create_items_query = "CREATE TABLE IF NOT EXISTS items (name VARCHAR, price real)"

cursor.execute(create_items_query)
connection.commit()
connection.close()