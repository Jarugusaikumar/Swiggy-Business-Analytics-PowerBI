TRUNCATE TABLE order_items CASCADE;
TRUNCATE TABLE orders CASCADE;
TRUNCATE TABLE menu CASCADE;
TRUNCATE TABLE restaurants CASCADE;
TRUNCATE TABLE users CASCADE;

\copy users (user_id,user_name,age,gender,marital_status,occupation)
FROM '__REPO_ROOT__/Data/raw/users.csv'
WITH CSV HEADER;

\copy restaurants (restaurant_id,restaurant_name,city,cuisine,rating,is_cloud_kitchen)
FROM '__REPO_ROOT__/Data/raw/restaurants.csv'
WITH CSV HEADER;

\copy menu (menu_id,restaurant_id,item_name,category,price,is_veg)
FROM '__REPO_ROOT__/Data/raw/menu.csv'
WITH CSV HEADER;

\copy orders (order_id,user_id,restaurant_id,order_date,delivery_time,order_status,payment_method,total_amount)
FROM '__REPO_ROOT__/Data/raw/orders.csv'
WITH CSV HEADER;

\copy order_items (order_item_id,order_id,menu_id,quantity,price)
FROM '__REPO_ROOT__/Data/raw/order_items.csv'
WITH CSV HEADER;
