import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os
import time

# ===============================
# Logging Configuration
# ===============================
LOG_DIR = "Logs"
LOG_FILE = "Create_Aggregated_table.log"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
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
# AGGREGATED TABLE CREATION QUERIES
# =====================================================================

# 1. Orders Master Table (Orders + Users + Restaurants)
CREATE_ORDERS_MASTER = """
DROP TABLE IF EXISTS orders_master CASCADE;

CREATE TABLE orders_master AS
WITH repeat_users AS (
    SELECT
        user_id,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY user_id
)
SELECT 
    -- Order Information
    o.order_id,
    o.order_date,
    o.delivery_time,
    o.order_status,
    o.payment_method,
    o.total_amount,
    
    -- User Information
    o.user_id,
    u.user_name,
    u.age,
    u.gender,
    u.marital_status,
    u.occupation,
    
    -- Age Group
    CASE 
        WHEN u.age < 18 THEN 'Under 18'
        WHEN u.age BETWEEN 18 AND 25 THEN '18-25'
        WHEN u.age BETWEEN 26 AND 35 THEN '26-35'
        WHEN u.age BETWEEN 36 AND 45 THEN '36-45'
        WHEN u.age BETWEEN 46 AND 55 THEN '46-55'
        WHEN u.age >= 56 THEN '56+'
        ELSE 'Unknown' -- Handles NULL values if they exist
    END as age_group,
    
    -- Repeat Customer
    CASE
        WHEN ru.total_orders > 1 THEN TRUE
        ELSE FALSE
    END AS is_repeat_customer,
    
    -- Restaurant Information
    o.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine,
    r.rating as restaurant_rating,
    
    -- Rating Category
    CASE 
        WHEN r.rating > 0 AND r.rating <= 2 THEN 'Poor'
        WHEN r.rating > 2 AND r.rating <= 3 THEN 'Average'
        WHEN r.rating > 3 AND r.rating <= 4 THEN 'Good'
        WHEN r.rating > 4 AND r.rating <= 4.5 THEN 'Very Good'
        WHEN r.rating > 4.5 AND r.rating <= 5 THEN 'Excellent'
        ELSE 'No Rating' -- Handles 0 or NULL values
    END AS rating_bucket,

    -- Restaurant Type
    CASE 
        WHEN r.is_cloud_kitchen = 1 THEN 'Cloud Kitchen'
        ELSE 'Traditional'
    END as restaurant_type,
    
    -- Derived Fields
    EXTRACT(YEAR FROM o.order_date) as order_year,
    EXTRACT(MONTH FROM o.order_date) as order_month,
    EXTRACT(QUARTER FROM o.order_date) as order_quarter,
    EXTRACT(DOW FROM o.order_date) as day_of_week,  -- 0=Sunday, 6=Saturday
    CASE 
        WHEN EXTRACT(DOW FROM o.order_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    
    CASE 
        WHEN EXTRACT(HOUR FROM o.delivery_time) BETWEEN 8 AND 11 THEN 'Breakfast'
        WHEN EXTRACT(HOUR FROM o.delivery_time) BETWEEN 12 AND 14 THEN 'Lunch'
        WHEN EXTRACT(HOUR FROM o.delivery_time) BETWEEN 15 AND 17 THEN 'Snack'
        WHEN EXTRACT(HOUR FROM o.delivery_time) BETWEEN 18 AND 22 THEN 'Dinner'
        ELSE 'Late Night'
    END as time_slot
    
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
LEFT JOIN repeat_users ru ON o.user_id = ru.user_id
INNER JOIN restaurants r ON o.restaurant_id = r.restaurant_id;
"""

CREATE_ORDERS_MASTER_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_om_user_id ON orders_master(user_id);
CREATE INDEX IF NOT EXISTS idx_om_restaurant_id ON orders_master(restaurant_id);
CREATE INDEX IF NOT EXISTS idx_om_order_status ON orders_master(order_status);
CREATE INDEX IF NOT EXISTS idx_om_order_date ON orders_master(order_date);
CREATE INDEX IF NOT EXISTS idx_om_year_month ON orders_master(order_year, order_month);
CREATE INDEX IF NOT EXISTS idx_om_city ON orders_master(city);
CREATE INDEX IF NOT EXISTS idx_om_cuisine ON orders_master(cuisine);
CREATE INDEX IF NOT EXISTS idx_om_is_repeat_customer ON orders_master(is_repeat_customer);
CREATE INDEX IF NOT EXISTS idx_om_rating_bucket ON orders_master(rating_bucket);
CREATE INDEX IF NOT EXISTS idx_om_restaurant_type ON orders_master(restaurant_type);
CREATE INDEX IF NOT EXISTS idx_om_age_group ON orders_master(age_group);
CREATE INDEX IF NOT EXISTS idx_om_day_type ON orders_master(day_type);
CREATE INDEX IF NOT EXISTS idx_om_time_slot ON orders_master(time_slot);
CREATE INDEX IF NOT EXISTS idx_om_payment_method ON orders_master(payment_method);

-- Customer Segmentation Queries
CREATE INDEX IF NOT EXISTS idx_om_repeat_status_date 
ON orders_master(is_repeat_customer, order_status, order_date);

-- Restaurant Performance Analysis
CREATE INDEX IF NOT EXISTS idx_om_type_rating_city 
ON orders_master(restaurant_type, rating_bucket, city);

-- Demographic Analysis
CREATE INDEX IF NOT EXISTS idx_om_status_age_date 
ON orders_master(order_status, age_group, order_date);

-- Time-based Operational Queries
CREATE INDEX IF NOT EXISTS idx_om_status_date_timeslot 
ON orders_master(order_status, order_date, time_slot);
"""

# 2. Order Items Master Table (Order Items + Menu)
CREATE_ORDER_ITEMS_MASTER = """
DROP TABLE IF EXISTS order_items_master CASCADE;

CREATE TABLE order_items_master AS
SELECT 
    -- Order Item Information
    oi.order_item_id,
    oi.order_id,
    oi.quantity,
    m.price as menu_price,
    (oi.quantity * m.price) as line_total,
    
    -- Menu Information
    oi.menu_id,
    m.restaurant_id,
    m.item_name,
    m.category,
    
    -- Derived Fields
    CASE 
        WHEN m.is_veg = 1 THEN 'Veg'
        ELSE 'Non-Veg'
    END as item_type,
    
    -- Price Category    
    CASE 
        WHEN m.price < 100 THEN 'Budget (<100)'
        WHEN m.price < 200 THEN 'Economic (100-199)'  
        WHEN m.price < 300 THEN 'Mid-Range (200-299)' 
        WHEN m.price < 400 THEN 'Premium (300-399)'   
        ELSE 'Luxury (400+)' 
    END as price_category
    
FROM order_items oi
INNER JOIN menu m ON oi.menu_id = m.menu_id;
"""

CREATE_ORDER_ITEMS_MASTER_INDEXES = """
CREATE INDEX idx_oim_order_id ON order_items_master(order_id);
CREATE INDEX idx_oim_menu_id ON order_items_master(menu_id);
CREATE INDEX idx_oim_restaurant_id ON order_items_master(restaurant_id);
CREATE INDEX idx_oim_category ON order_items_master(category);
CREATE INDEX idx_oim_item_type ON order_items_master(item_type);
CREATE INDEX idx_oim_price_category ON order_items_master(price_category);
"""

# ===============================
# Database Connection
# ===============================
def create_connection():
    try:
        logging.info("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logging.info("Database connection established successfully.\n")
        return conn
    
    except Exception as e:
        # Show Logs error details & Stops execution if DB fails
        logging.error(f"Database connection failed: {e}\n") 
        raise

# -------------------------------
# Create Aggregated Tables
# -------------------------------
def create_aggregated_table(conn): 
    logging.info("=" * 70)
    logging.info("CREATING AGGREGATED TABLES")
    logging.info("=" * 70)
    
    cursor = conn.cursor()
    
    tables = [
        (CREATE_ORDERS_MASTER, "orders_master Table"),
        (CREATE_ORDERS_MASTER_INDEXES, "orders_master Indexes"),
        (CREATE_ORDER_ITEMS_MASTER, "order_items_master Table"),
        (CREATE_ORDER_ITEMS_MASTER_INDEXES, "order_items_master Indexes")
    ]
    
    success_count = 0
    
    for query, name in tables:
        try:
            execute_query(cursor, query, name)
            success_count += 1
        except Exception as e:
            logging.error(f"Skipping {name} due to error")
    
    cursor.close()
    
    # Verification
    logging.info("=" * 70)
    logging.info("VERIFICATION")
    logging.info("=" * 70)
    
    verify_tables = ['orders_master', 'order_items_master']
    
    for table_name in verify_tables:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            logging.info(f"{table_name}: {count:,} rows")
        except Exception as e:
            logging.error(f"{table_name}: Verification failed")
        finally:
            cursor.close()
    
    logging.info("=" * 70)
    logging.info(f"SUMMARY: {success_count}/{len(tables)} operations successful")
    logging.info("=" * 70 + "\n")

# -------------------------------
# Drop Tables
# -------------------------------
def drop_all_tables(conn):
    logging.info("=" * 70)
    logging.info("DROPPING EXISTING TABLES")
    logging.info("=" * 70)
    
    start_time = time.time()
    cursor = conn.cursor()
    
    drop_queries = [
        ("DROP TABLE IF EXISTS order_items_master", "order_items_master"),
        ("DROP TABLE IF EXISTS orders_master", "orders_master")
    ]
    
    dropped_count = 0
    
    for query, name in drop_queries:
        try:
            # Get row count before dropping (if table exists)
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {name};")
                row_count = cursor.fetchone()[0]
                logging.info(f"Table {name} exists with {row_count:,} rows")
            except:
                logging.info(f"Table {name} does not exist yet")
                row_count = None
            
            # Drop the table
            cursor.execute(f"{query} CASCADE;")
            
            if row_count is not None:
                logging.info(f"Dropped table: {name} ({row_count:,} rows)")
            else:
                logging.info(f"Dropped table: {name} (was empty/non-existent)")
            
            dropped_count += 1
        
        except Exception as e:
            logging.warning(f"Could not drop table {name}: {str(e)}")
    
    cursor.close()

    elapsed_time = time.time() - start_time
    
    logging.info("=" * 70)
    logging.info(f"Dropped {dropped_count}/{len(drop_queries)} tables in {elapsed_time:.2f}s")
    logging.info("=" * 70 + "\n")

# -------------------------------
# Execute Queries
# -------------------------------  
def execute_query(cursor,query,query_name): 
    try:
        start_time = time.time()
        logging.info(f"Executing: {query_name} Query")
        cursor.execute(query)
        elapsed_time = round(time.time() - start_time, 2)
        
        # If it's a table creation (not index), get row count
        if "Table" in query_name and "Indexes" not in query_name:
            table_name = query_name.split()[0]  # Extract table name
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            logging.info(
                f"{query_name} created successfully: "
                f"{row_count:,} rows in {elapsed_time:.2f}s"
            )
        else:
            logging.info(
                f"{query_name} created successfully in {elapsed_time:.2f}s"
            )
    
    except Exception as e:
        logging.error(f"Failed to execute {query_name}: {str(e)}")
        raise

# ===============================
# Main Execution Flow
# ===============================
def main():
    start_time = time.time()
    
    logging.info("=" * 70)
    logging.info("AGGREGATED TABLES CREATION STARTED")
    logging.info("=" * 70)
    
    conn = None
    
    try:
        # Connect
        conn = create_connection()
        
        # Drop existing aggregated tables
        drop_all_tables(conn)
        
        # Create new aggregated tables
        create_aggregated_table(conn)
        
        total_time = time.time() - start_time
        
        logging.info("=" * 70)
        logging.info("AGGREGATED TABLES CREATION COMPLETED")
        logging.info(f"Total time: {total_time:.2f} seconds")
        logging.info("=" * 70 + "\n")
        
    except Exception as e:
        logging.error("=" * 70)
        logging.error("AGGREGATED TABLES CREATION FAILED")
        logging.error(f"Error: {str(e)}")
        logging.info("=" * 70 + "\n")
        raise
        
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed")

# -------------------------------
# Run Script
# -------------------------------
if __name__ == "__main__":
    try:
        main()
        
        print("\n" + "=" * 70)
        print("AGGREGATED TABLES CREATED SUCCESSFULLY!")
        print(f"Log: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        
    except Exception:
        print("\n" + "=" * 70)
        print("ERROR: Creation failed!")
        print(f"Check log: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        exit(1)
