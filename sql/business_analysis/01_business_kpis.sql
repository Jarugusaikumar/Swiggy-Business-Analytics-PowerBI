-- Business analysis queries for Swiggy operations analytics

-- 1. Monthly revenue trend
SELECT TO_CHAR(order_date, 'YYYY-MM') AS month_key,
       ROUND(SUM(total_amount), 2) AS monthly_revenue,
       COUNT(*) AS order_count
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month_key;

-- 2. Revenue by city
SELECT r.city,
       ROUND(SUM(o.total_amount), 2) AS total_revenue,
       COUNT(*) AS total_orders
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city
ORDER BY total_revenue DESC;

-- 3. Top restaurants by revenue
SELECT r.restaurant_name,
       r.city,
       ROUND(SUM(o.total_amount), 2) AS revenue,
       COUNT(*) AS total_orders
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_name, r.city
ORDER BY revenue DESC
LIMIT 10;

-- 4. Top customers by revenue
SELECT u.user_id,
       u.user_name,
       ROUND(SUM(o.total_amount), 2) AS customer_revenue,
       COUNT(*) AS order_count
FROM orders o
JOIN users u ON u.user_id = o.user_id
GROUP BY u.user_id, u.user_name
ORDER BY customer_revenue DESC
LIMIT 10;

-- 5. Cancellation rate
SELECT ROUND(
    (SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) /
    COUNT(*),
    2
) AS cancellation_rate_pct
FROM orders;

-- 6. Average order value
SELECT ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders;

-- 7. Customer order frequency
SELECT u.user_id,
       u.user_name,
       COUNT(*) AS order_count,
       ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM users u
JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.user_name
ORDER BY order_count DESC
LIMIT 20;

-- 8. Restaurant performance
SELECT r.restaurant_name,
       r.city,
       ROUND(AVG(r.rating), 2) AS avg_rating,
       COUNT(o.order_id) AS total_orders,
       ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM restaurants r
LEFT JOIN orders o ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name, r.city
ORDER BY total_revenue DESC;

-- 9. Year-over-year revenue growth
WITH sales_by_year AS (
    SELECT EXTRACT(YEAR FROM order_date) AS order_year,
           ROUND(SUM(total_amount), 2) AS yearly_revenue
    FROM orders
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT order_year,
       yearly_revenue,
       LAG(yearly_revenue) OVER (ORDER BY order_year) AS previous_year_revenue,
       ROUND(((yearly_revenue - LAG(yearly_revenue) OVER (ORDER BY order_year)) /
              NULLIF(LAG(yearly_revenue) OVER (ORDER BY order_year), 0)) * 100, 2) AS yoy_growth_pct
FROM sales_by_year;
