import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME"),
            'port': int(os.getenv("DB_PORT")),
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.create_tables()

    def connect(self):
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=()):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    def fetch_query(self, query, params=()):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def create_tables(self):
        self.execute_query('''CREATE TABLE IF NOT EXISTS categories (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL UNIQUE)''')
        self.execute_query('''CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, image_url TEXT, price DECIMAL(10, 2) NOT NULL, category_id INT, FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL)''')
        self.execute_query('''CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, table_number VARCHAR(10) NOT NULL, user_name VARCHAR(100) NOT NULL, status VARCHAR(50) DEFAULT 'IN_ATTESA', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.execute_query('''CREATE TABLE IF NOT EXISTS order_items (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_id INT, quantity INT NOT NULL, FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE, FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)''')

    def get_all_categories(self): 
        return self.fetch_query("SELECT * FROM categories")
        
    def get_all_products(self): 
        return self.fetch_query("SELECT p.*, c.name as category_name FROM products p JOIN categories c ON p.category_id = c.id")

    def add_product(self, name, image_url, price, category_id):
        self.execute_query("INSERT INTO products (name, image_url, price, category_id) VALUES (%s, %s, %s, %s)", (name, image_url, price, category_id))

    def update_product(self, pid, name, image_url, price, category_id):
        self.execute_query("UPDATE products SET name=%s, image_url=%s, price=%s, category_id=%s WHERE id=%s", (name, image_url, price, category_id, pid))

    def delete_product(self, pid):
        self.execute_query("DELETE FROM products WHERE id = %s", (pid,))

    def add_order(self, table, user):
        query = "INSERT INTO orders (table_number, user_name) VALUES (%s, %s)"
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (table, user))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    def add_order_item(self, order_id, product_id, quantity):
        self.execute_query("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)", (order_id, product_id, quantity))

    def get_orders_staff(self):
        return self.fetch_query('''SELECT o.*, GROUP_CONCAT(CONCAT(p.name, ' x', oi.quantity) SEPARATOR ', ') as details FROM orders o JOIN order_items oi ON o.id = oi.order_id JOIN products p ON oi.product_id = p.id GROUP BY o.id ORDER BY o.created_at DESC''')

    def update_order_status(self, order_id, status):
        self.execute_query("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))