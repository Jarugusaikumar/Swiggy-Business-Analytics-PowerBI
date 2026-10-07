import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os 
import time

LOG_DIR = "Logs"
LOG_FILE = "Insert_data.log"

# Creates Logs/ folder if it doesn’t exist
os.makedirs(LOG_DIR, exist_ok=True) 

# Basic Config of Logging
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

# -------------------------------
# CSV File Paths
# -------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "Data")

CSV_FILES = [
    ("users" , "users.csv"),
    ("restaurants" , "restaurants.csv"),
    ("menu" , "menu.csv"),
    ("orders" , "orders.csv"),
    ("order_items" , "order_items.csv")
]

# -------------------------------
# Validate CSV File
# -------------------------------
def validate_csv_files():
    """Verify all CSV files exist before starting"""
    logging.info("Validating CSV files...")
    
    all_exist = True
    for table_name, csv_file in CSV_FILES:
        file_path = os.path.join(DATA_PATH, csv_file)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            logging.info(f"Found: {csv_file} ({file_size:.2f} MB)")
        else:
            logging.error(f"Missing: {csv_file}")
            all_exist = False
    
    if not all_exist:
        raise FileNotFoundError("Some CSV files are missing!")
    
    logging.info("All CSV files validated successfully.\n")

# -------------------------------
# Connect to PostgreSQL
# -------------------------------
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
# Truncate Tables
# -------------------------------
def truncate_tables(conn):
    try:
        cursor = conn.cursor()
        
        logging.info("=" * 70)
        logging.info("TRUNCATING TABLES")
        logging.info("=" * 70)

        truncate_queries = [
            ("order_items", "TRUNCATE TABLE order_items CASCADE;"),
            ("orders", "TRUNCATE TABLE orders CASCADE;"),
            ("menu", "TRUNCATE TABLE menu CASCADE;"),
            ("restaurants", "TRUNCATE TABLE restaurants CASCADE;"),
            ("users", "TRUNCATE TABLE users CASCADE;")
        ]

        for table_name, query in truncate_queries:
            # Get row count before truncate
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            before_count = cursor.fetchone()[0]
            
            # Truncate Table
            cursor.execute(query)
            
            # Verify truncate
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            after_count = cursor.fetchone()[0]
            
            logging.info(
                f"Truncated {table_name}: "
                f"{before_count:,} rows deleted, {after_count} remaining"
            )

        cursor.close()
        logging.info("=" * 70)
        logging.info("All tables truncated successfully")
        logging.info("=" * 70 + "\n")

    except Exception as e:
        logging.error(f"Error during table truncation: {e}\n")
        raise

# -------------------------------
# Insert Data into Tables
# -------------------------------
def insert_csv(table_name, csv_file, conn):
    start_time = time.time()

    try:
        cursor = conn.cursor()
        file_path = os.path.join(DATA_PATH, csv_file)
        
        # Get file size for logging
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        logging.info(
            f"Started inserting '{csv_file}' data into '{table_name}' "
            f"(File size: {file_size:.2f} MB)"
        )
        
        # Get row count before insert
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        before_count = cursor.fetchone()[0]

        with open(file_path, 'r', encoding='utf-8') as f:
            cursor.copy_expert(
                sql=f"""
                COPY {table_name}
                FROM STDIN
                WITH CSV HEADER
                """,
                file=f
            )
            
        # Get row count after insert
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        after_count = cursor.fetchone()[0]
        rows_inserted = after_count - before_count

        elapsed_time = round(time.time() - start_time, 2)
        
        # Calculate insertion rate
        rows_per_second = int(rows_inserted / elapsed_time) if elapsed_time > 0 else 0
        
        logging.info(
            f"Completed '{table_name}': "
            f"{rows_inserted:,} rows inserted in {elapsed_time}s "
            f"({rows_per_second:,} rows/sec)"
        )

        cursor.close()
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except psycopg2.Error as e:
        logging.error(f"PostgreSQL error inserting {csv_file}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error inserting {csv_file}: {e}")
        raise

# -------------------------------
# Main Execution Flow
# -------------------------------
def main():
    start_time = time.time()
    
    logging.info("=" * 70)
    logging.info("DATA INSERTION PROCESS STARTED")
    logging.info("=" * 70)

    conn = None
    success_count = 0

    try:
        # Validate CSV files exist
        validate_csv_files()
        
        # Connect to database
        conn = create_connection()
        
        # Clear existing data
        truncate_tables(conn)
        
        # Insert data from CSV files
        for table_name, csv_file in CSV_FILES:
            insert_csv(table_name, csv_file, conn)
            success_count += 1
        
        # Calculate total time
        total_time = time.time() - start_time
        
        logging.info("=" * 70)
        logging.info("DATA INSERTION SUMMARY")
        logging.info("=" * 70)
        logging.info(f"Tables processed: {len(CSV_FILES)}")
        logging.info(f"Successful: {success_count}")
        logging.info(f"Failed: {len(CSV_FILES) - success_count}")
        logging.info(f"Total time: {total_time:.2f} seconds\n")
        logging.info("=" * 70)
        logging.info("DATA INSERTION COMPLETED SUCCESSFULLY")
        logging.info("=" * 70 + "\n")

    except Exception as e:
        logging.error("=" * 70)
        logging.error("DATA INSERTION FAILED")
        logging.error(f"Error: {str(e)}")
        logging.error("=" * 70 + "\n")
        raise
        
    finally:
        # Always close connection
        if conn:
            conn.close()
            logging.info("Database connection closed.")

# -------------------------------
# Run Script
# -------------------------------
if __name__ == "__main__":    
    try:
        main()
        
        print("\n" + "=" * 70)
        print("DATA INSERTION COMPLETED SUCCESSFULLY!")
        print(f"Check logs: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("ERROR: Data insertion failed!")
        print(f"Check logs for details: {os.path.join(LOG_DIR, LOG_FILE)}")
        print("=" * 70 + "\n")
        exit(1)  # Exit with error code
