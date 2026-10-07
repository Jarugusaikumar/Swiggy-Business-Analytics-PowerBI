import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os 
import time

# ===============================
# Logging Configuration
# ===============================
LOG_DIR = "Logs"
LOG_FILE = "Create_tables.log"

# Creates Logs/ folder if it doesn’t exist
os.makedirs(LOG_DIR, exist_ok=True) 

logging.basicConfig(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------
# Database Configuration
# -------------------------------
DB_NAME = "swiggy"
DB_USER = "postgres"
DB_PASSWORD = "your_password" # Replace this with Your Password 
DB_HOST = "localhost"
DB_PORT = "5432"

# =====================================================================
# TABLE CREATION QUERIES
# =====================================================================

# 1. Users Table
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    marital_status VARCHAR(20) NOT NULL,
    occupation VARCHAR(50) NOT NULL
);
"""

CREATE_USERS_INDEXES = """
    CREATE INDEX IF NOT EXISTS idx_users_age ON users(age);
    CREATE INDEX IF NOT EXISTS idx_users_gender ON users(gender);
    CREATE INDEX IF NOT EXISTS idx_users_occupation ON users(occupation);
    CREATE INDEX IF NOT EXISTS idx_users_marital_status ON users(marital_status);
"""

# 2. Restaurants Table
CREATE_RESTAURANTS_TABLE = """
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id VARCHAR(10) PRIMARY KEY,
    restaurant_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine VARCHAR(50) NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    is_cloud_kitchen INT NOT NULL
);
"""

CREATE_RESTAURANTS_INDEXES = """
    CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city);
    CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine ON restaurants(cuisine);
    CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating);
    CREATE INDEX IF NOT EXISTS idx_restaurants_cloud_kitchen ON restaurants(is_cloud_kitchen);
"""

# 3. Menu Table
CREATE_MENU_TABLE = """
CREATE TABLE IF NOT EXISTS menu (
    menu_id VARCHAR(10) PRIMARY KEY,
    restaurant_id VARCHAR(10) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_veg SMALLINT NOT NULL,
    
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);
"""

CREATE_MENU_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_menu_restaurant ON menu(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_menu_category ON menu(category);
CREATE INDEX IF NOT EXISTS idx_menu_price ON menu(price);
CREATE INDEX IF NOT EXISTS idx_menu_is_veg ON menu(is_veg);
"""

# 4. Orders Table
CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(15) PRIMARY KEY,
    user_id VARCHAR(10) NOT NULL,
    restaurant_id VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    delivery_time TIME NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);
"""

CREATE_ORDERS_INDEXES = """
    CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
    CREATE INDEX IF NOT EXISTS idx_orders_restaurant ON orders(restaurant_id);
    CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
    CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);
    CREATE INDEX IF NOT EXISTS idx_orders_payment ON orders(payment_method);
    CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(order_date, order_status);
"""

# 5. Order Items Table
CREATE_ORDER_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id VARCHAR(15) PRIMARY KEY,
    order_id VARCHAR(15) NOT NULL,
    menu_id VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON DELETE CASCADE
);
"""

CREATE_ORDER_ITEMS_INDEXES = """
    CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
    CREATE INDEX IF NOT EXISTS idx_order_items_menu ON order_items(menu_id);
"""

# -------------------------------
# Connect to PostgreSQL
# -------------------------------
def create_connection():
    try:
        logging.info("Connecting to PostgreSQL Database...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logging.info("Database connection Established Successfully.\n")
        return conn
    
    except Exception as e:
        # Show Logs error details & Stops execution if DB fails
        logging.error(f"Database Connection Failed: {e}\n") 
        raise

# -------------------------------
# Execute Query
# -------------------------------    
def execute_query(cursor,query, query_name):
    try:
        logging.info(f"Executing: {query_name} Query")
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"{query_name} Created Successfully ({duration:.2f}s).")
    
    except Exception as e:
        logging.error(f"Failed to Execute {query_name} Query : {str(e)}")
        raise

# -------------------------------
# Create Tables
# -------------------------------
def create_all_tables(conn):
    logging.info("=" * 70)
    logging.info("Starting Table Creation Process...")
    logging.info("=" * 70)
    cursor = conn.cursor()
    
    tables = [
        (CREATE_USERS_TABLE, "Users Table"),
        (CREATE_USERS_INDEXES, "Users Indexes"),
        (CREATE_RESTAURANTS_TABLE, "Restaurants Table"),
        (CREATE_RESTAURANTS_INDEXES, "Restaurants Indexes"),
        (CREATE_MENU_TABLE, "Menu Table"),
        (CREATE_MENU_INDEXES, "Menu Indexes"),
        (CREATE_ORDERS_TABLE, "Orders Table"),
        (CREATE_ORDERS_INDEXES, "Orders Indexes"),
        (CREATE_ORDER_ITEMS_TABLE, "Order_items Table"),
        (CREATE_ORDER_ITEMS_INDEXES, "Order_items Indexes"),
    ]
    
    success_count = 0
    failed_count = 0
    
    for query, name in tables:
        try:
            execute_query(cursor, query, name)
            success_count += 1
        except Exception as e:
            failed_count += 1
            logging.error(f"Skipping {name} due to error")
        
    cursor.close()
    logging.info("=" * 70)
    logging.info("TABLE CREATION SUMMARY")
    logging.info("=" * 70)
    logging.info(f"Total operations: {len(tables)}")
    logging.info(f"Successful: {success_count}")
    logging.info(f"Failed: {failed_count}")
    logging.info("=" * 70 + "\n")
    
    if failed_count == 0:
        logging.info("All tables & indexes created successfully!\n")
    else:
        logging.warning(f"{failed_count} operation(s) failed. Check logs above.\n")

# -------------------------------
# Drop Tables
# -------------------------------
def drop_all_tables(conn):
    logging.info("=" * 70)
    logging.info("DROPPING EXISTING TABLES")
    logging.info("=" * 70)
    cursor = conn.cursor()
    drop_queries = [
        ("DROP TABLE IF EXISTS order_items", "order_items"),
        ("DROP TABLE IF EXISTS orders", "orders"),
        ("DROP TABLE IF EXISTS menu", "menu"),
        ("DROP TABLE IF EXISTS restaurants", "restaurants"),
        ("DROP TABLE IF EXISTS users", "users"),
    ]
    
    dropped_count = 0
    
    for query, name in drop_queries:
        try:
            cursor.execute(f"{query} CASCADE;")
            logging.info(f"Dropped table: {name}")
            dropped_count += 1
        
        except Exception as e:
            logging.warning(f"Table {name} not found (probably doesn't exist yet)")
    
    cursor.close()

    logging.info("=" * 70)
    logging.info(f"Dropped {dropped_count}/{len(drop_queries)} tables")
    logging.info("=" * 70 + "\n")

# -------------------------------
# Run Script
# -------------------------------
if __name__ == "__main__":
    start_time = time.time()
    
    logging.info("=" * 70)
    logging.info("SWIGGY DATABASE SETUP - STARTING")
    logging.info("=" * 70)
    
    conn = None
    
    try:
        # Connect to database
        conn = create_connection()
        
        # Drop existing tables
        drop_all_tables(conn)
        
        # Create all tables and indexes
        create_all_tables(conn)
        
        # Success message
        end_time = time.time()
        duration = end_time - start_time
        
        logging.info("=" * 70)
        logging.info("DATABASE SETUP COMPLETED SUCCESSFULLY")
        logging.info(f"Total time: {duration:.2f} seconds")
        logging.info("=" * 70 + "\n")
        
        print("\n" + "=" * 70)
        print("All Tables & Indexes Created Successfully!")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Check logs: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logging.error("=" * 70)
        logging.error("DATABASE SETUP FAILED")
        logging.error(f"Error: {str(e)}")
        logging.error("=" * 70 + "\n")
        
        print("\n" + "=" * 70)
        print("ERROR: Database setup failed!")
        print(f"Check logs for details: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        
    finally:
        # Always close connection
        if conn:
            conn.close()
            logging.info("Database connection closed.")
