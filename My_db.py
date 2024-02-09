import tkinter as tk
from tkinter import messagebox
import sqlite3
import getpass

def connect_to_database(special_db): 
    conn = sqlite3.connect(special_db) #here anyone using this can modify the path to the desired file where the database should be located 
    return conn

def create_products_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            last_modified TEXT
        )
    ''')
    conn.commit()

# adding a product to the database and display the message using messagebox in tkinter (this messagebox brings back memories from 2000)
def add_product(conn, name, quantity, price, last_modified):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, quantity, price, last_modified) VALUES (?, ?, ?, ?)
    ''', (name, quantity, price, last_modified))
    conn.commit()
    messagebox.showinfo("Success", "Product added successfully!")

def retrieve_products(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return products

def delete_product(conn, product_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    messagebox.showinfo("Success", "Product deleted successfully!")


# Function to create the GUI and handle adding a product using get() method
def add_product_gui():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    username = getpass.getuser()
    add_product(conn, name, quantity, price, username)

def delete_product_gui():
    product_id = int(product_id_entry.get())
    delete_product(conn, product_id)


special_db = 'inventory.db'
conn = connect_to_database(special_db)
create_products_table(conn)

# Tkinter window
window = tk.Tk()
window.title("Inventory Management")

# labels and entry fields
name_label = tk.Label(window, text="Product Name:")
name_label.grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=5)

quantity_label = tk.Label(window, text="Quantity:")
quantity_label.grid(row=1, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(window)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

price_label = tk.Label(window, text="Price:")
price_label.grid(row=2, column=0, padx=10, pady=5)
price_entry = tk.Entry(window)
price_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(window, text="Add Product", command=add_product_gui)
add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

product_id_label = tk.Label(window, text="Product ID to Delete:")
product_id_label.grid(row=4, column=0, padx=10, pady=5)
product_id_entry = tk.Entry(window)
product_id_entry.grid(row=4, column=1, padx=10, pady=5)

def show_inventory():
    products = retrieve_products(conn)
    if products:
        messagebox.showinfo("Inventory", "\n".join([f"Name: {product[1]}\nQuantity: {product[2]}\nPrice: {product[3]}\nLast Modified By: {product[4]}" for product in products]))
    else:
        messagebox.showinfo("Inventory", "No products found!")

# Create and place the "Show Inventory" button as well as delete button
show_inventory_button = tk.Button(window, text="Show Inventory", command=show_inventory)
show_inventory_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

delete_button = tk.Button(window, text="Delete Product", command=delete_product_gui)
delete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")


window.mainloop()
