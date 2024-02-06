import sqlite3
import getpass

def connect_to_database(special_db):
    conn = sqlite3.connect(special_db)
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

def add_product(conn, name, quantity, price, last_modified):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, quantity, price, last_modified) VALUES (?, ?, ?, ?)
    ''', (name, quantity, price, last_modified))
    conn.commit()

def retrieve_products(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return products

def update_product(conn, product_id, name, quantity, price, last_modified):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE products SET name=?, quantity=?, price=? WHERE id=?, last_modified
    ''', (name, quantity, price, product_id, last_modified))
    conn.commit()


def delete_product(conn, product_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()



#Creating main function:
    
def main():
    special_db = 'inventory.db'
    conn = connect_to_database(special_db)
    create_products_table(conn)

    while True:
        print("\nOptions:")
        print("1. Add Product")
        print("2. Retrieve Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            username = getpass.getuser() 
            add_product(conn, name, quantity, price, username)
            print("Product added successfully!")

        elif choice == '2':
            products = retrieve_products(conn)
            if products:
                print("\nAll Products:")
                for product in products:
                    print(product)
            else:
                print("No products found!")

        elif choice == '3':
            product_id = int(input("Enter product ID to update: "))
            name = input("Enter new name: ")
            quantity = int(input("Enter new quantity: "))
            price = float(input("Enter new price: "))
            username = getpass.getuser()
            update_product(conn, product_id, name, quantity, price, username)
            print("Product updated successfully!")

        elif choice == '4':
            product_id = int(input("Enter product ID to delete: "))
            delete_product(conn, product_id)
            print("Product deleted successfully!")

        elif choice == '5':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
