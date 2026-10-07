-- Data quality checks for Swiggy analytics

-- 1. Null and empty checks
SELECT 'users' AS table_name, COUNT(*) AS null_or_blank_rows
FROM users
WHERE user_id IS NULL OR user_name IS NULL OR age IS NULL
UNION ALL
SELECT 'restaurants', COUNT(*)
FROM restaurants
WHERE restaurant_id IS NULL OR restaurant_name IS NULL OR city IS NULL
UNION ALL
SELECT 'orders', COUNT(*)
FROM orders
WHERE order_id IS NULL OR user_id IS NULL OR restaurant_id IS NULL OR total_amount IS NULL;

-- 2. Duplicate key checks
SELECT 'users' AS table_name, COUNT(*) - COUNT(DISTINCT user_id) AS duplicate_keys
FROM users
UNION ALL
SELECT 'restaurants', COUNT(*) - COUNT(DISTINCT restaurant_id)
FROM restaurants
UNION ALL
SELECT 'orders', COUNT(*) - COUNT(DISTINCT order_id)
FROM orders;

-- 3. Invalid order statuses
SELECT COUNT(*) AS invalid_status_rows
FROM orders
WHERE order_status NOT IN ('Delivered', 'Cancelled');

-- 4. Revenue sanity check
SELECT MIN(total_amount) AS min_order_value,
       AVG(total_amount) AS avg_order_value,
       MAX(total_amount) AS max_order_value
FROM orders;

-- 5. Date field validation
SELECT COUNT(*) AS invalid_order_dates
FROM orders
WHERE order_date IS NULL OR order_date > CURRENT_DATE;
