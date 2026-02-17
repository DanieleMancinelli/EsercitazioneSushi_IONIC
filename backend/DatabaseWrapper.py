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
        # Tabella Categorie (es. Nigiri, Bibite)
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            )
        ''')
        
        # Tabella Prodotti
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                image_url TEXT,
                price DECIMAL(10, 2) NOT NULL,
                category_id INT,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        ''')
        
        # Tabella Ordini (Comande)
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                table_number VARCHAR(10) NOT NULL,
                user_name VARCHAR(100) NOT NULL,
                status VARCHAR(50) DEFAULT 'IN_ATTESA',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella Dettaglio Ordine (Piatti specifici ordinati)
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        ''')

    # Metodi che verranno usati dalle API (Senza SQL in app.py)
    def get_all_categories(self):
        return self.fetch_query("SELECT * FROM categories")

    def get_all_products(self):
        return self.fetch_query("SELECT p.*, c.name as category_name FROM products p JOIN categories c ON p.category_id = c.id")

    def add_order(self, table_number, user_name):
        query = "INSERT INTO orders (table_number, user_name) VALUES (%s, %s)"
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (table_number, user_name))
                conn.commit()
                return cursor.lastrowid # Ci servirà per sapere a quale ordine aggiungere i piatti
        finally:
            conn.close()

