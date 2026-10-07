# 🍔 SWIGGY SALES ANALYSIS - DATA GENERATION DOCUMENTATION

## Complete Guide to Synthetic Data Generation

---

## 📑 TABLE OF CONTENTS

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Quick Start Guide](#quick-start-guide)
4. [Data Generation Architecture](#data-generation-architecture)
5. [Configuration Parameters](#configuration-parameters)
6. [Data Schema Design](#data-schema-design)
7. [Generation Logic & Algorithms](#generation-logic--algorithms)
8. [Realistic Patterns Implementation](#realistic-patterns-implementation)
9. [Data Quality & Validation](#data-quality--validation)
10. [Performance Optimization](#performance-optimization)
11. [Troubleshooting](#troubleshooting)
12. [Advanced Customization](#advanced-customization)
13. [FAQs](#faqs)

---

## 📖 OVERVIEW

### Purpose

This data generation script creates a realistic, synthetic dataset for a food delivery platform (Swiggy) that can be used for:

- **Data Analysis Projects** - End-to-End Analytics Portfolio
- **SQL Practice** - Complex Query development
- **Business Intelligence** - Dashboard creation in Power BI
- **Machine Learning** - Predictive modeling
- **Interview Preparation** - Demonstrating technical skills

### Key Features

✅ **Large Scale** - Generates 600,000+ orders with 1.67M+ line items  
✅ **Realistic Patterns** - Implements real-world business logic  
✅ **High Performance** - Optimized for speed using vectorization  
✅ **Data Integrity** - Maintains referential integrity across tables  
✅ **Customizable** - Easy configuration for different scenarios  
✅ **Reproducible** - Seed-based generation for consistency

### Generated Dataset Summary

| Metric | Value |
|--------|-------|
| **Users** | 10,000 |
| **Restaurants** | 1,000 |
| **Menu Items** | ~15,658 |
| **Orders** | 600,000 |
| **Order Items** | ~1,667,399 |
| **Time Period** | 4 years (2022-2025) |
| **File Size** | ~128 MB total |

---

## 💻 SYSTEM REQUIREMENTS

### Minimum Requirements

```
- Python: 3.8 or higher
- RAM: 4 GB minimum
- Disk Space: 500 MB free
- OS: Windows, macOS, or Linux
```

### Recommended Requirements

```
- Python: 3.10+
- RAM: 8 GB or more
- Disk Space: 1 GB free
- CPU: Multi-core processor
```

### Required Python Libraries

```python
pandas>=1.3.0
numpy>=1.21.0
```

### Installation

```bash
# Install required libraries
pip install pandas numpy

# Or using requirements.txt
pip install -r requirements.txt
```

---

## 🚀 QUICK START GUIDE

### Step 1: Download the Script

Save the `swiggy_data_generator.py` file to your working directory.

### Step 2: Run the Script

```bash
# Navigate to directory
cd /path/to/your/directory

# Run the script
python swiggy_data_generator.py
```

### Step 3: Output

The script will generate 5 CSV files:

```
✓ users.csv          - Customer data
✓ restaurants.csv    - Restaurant information
✓ menu.csv           - Menu items
✓ orders.csv         - Order transactions
✓ order_items.csv    - Order line items
```

### Expected Runtime

| Dataset Size | Approximate Time |
|-------------|------------------|
| 100K orders | 10-15 seconds |
| 600K orders | 30-60 seconds |
| 1M orders | 1-2 minutes |

---

## 🏗️ DATA GENERATION ARCHITECTURE

### Process Flow

```
┌─────────────────────────────────────────────────────────┐
│                  1. CONFIGURATION                       │
│  Set parameters (users, restaurants, orders, dates)     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  2. GENERATE USERS                      │
│  Create customer profiles with demographics             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                3. GENERATE RESTAURANTS                  │
│  Create restaurant profiles with locations              │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  4. GENERATE MENU                       │
│  Create menu items for each restaurant                  │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  5. GENERATE ORDERS                     │
│  Create order transactions with realistic patterns      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                6. GENERATE ORDER ITEMS                  │
│  Create line items and calculate order totals           │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  7. SAVE TO CSV FILES                   │
│  Export all tables to CSV format                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  8. GENERATE STATISTICS                 │
│  Print summary and validation metrics                   │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

```python
┌─────────────────────────────────────────┐
│          Data Generation Layer          │
│                                         │
│  ┌─────────────┐    ┌──────────────┐    │
│  │   NumPy     │    │   Random     │    │
│  │ Vectorized  │    │  Seeding     │    │
│  │ Operations  │    │  Control     │    │
│  └─────────────┘    └──────────────┘    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Data Manipulation Layer           │
│                                         │
│  ┌─────────────┐    ┌──────────────┐    │
│  │   Pandas    │    │  DateTime    │    │
│  │ DataFrames  │    │  Handling    │    │
│  │ Operations  │    │              │    │
│  └─────────────┘    └──────────────┘    │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│          Output Layer (CSV)             │
└─────────────────────────────────────────┘
```

---

## ⚙️ CONFIGURATION PARAMETERS

### Basic Configuration

Located at the top of the script:

```python
# =====================================================================
# CONFIGURATION - Adjust these parameters
# =====================================================================
NUM_USERS = 10000          # Number of customers to generate
NUM_RESTAURANTS = 1000     # Number of restaurants to generate
NUM_ORDERS = 600000        # Number of orders to generate
START_DATE = datetime(2022, 1, 1)   # Start date for orders
END_DATE = datetime(2025, 12, 31)   # End date for orders
```

### Parameter Guidelines

#### NUM_USERS

**Range:** 1,000 - 100,000

**Recommendations:**
- **Small Dataset**: 1,000-5,000 users
- **Medium Dataset**: 5,000-20,000 users
- **Large Dataset**: 20,000-100,000 users

**Impact:**
- Higher = More diverse customer base
- Lower = Faster generation, smaller files

**Business Logic:**
- 20% of users will be "heavy users" (80-20 rule)
- Age range: 18-64 years
- Gender split: 55% Male, 45% Female

#### NUM_RESTAURANTS

**Range:** 100 - 10,000

**Recommendations:**
- **Small City**: 100-500 restaurants
- **Medium City**: 500-2,000 restaurants
- **Large City**: 2,000-10,000 restaurants

**Impact:**
- Higher = More menu variety
- Lower = Faster generation

**Business Logic:**
- Distributed across 10 cities with weights
- 70% traditional, 30% cloud kitchens
- Rating distribution: mostly 3.5-4.5

#### NUM_ORDERS

**Range:** 10,000 - 10,000,000

**Recommendations:**
- **Testing**: 10,000-50,000 orders
- **Analysis**: 100,000-500,000 orders
- **Big Data**: 500,000-10,000,000 orders

**Impact:**
- Higher = Longer generation time
- Higher = Larger file sizes
- Higher = Better statistical analysis

**Calculation:**
```
Average order items = 2.78 per order
Total order items ≈ NUM_ORDERS × 2.78

Example:
600,000 orders × 2.78 ≈ 1,668,000 order items
```

#### Date Range

**START_DATE / END_DATE**

**Recommendations:**
```python
# 1 year of data
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

# 2 years of data
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# 4 years of data (current setting)
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2025, 12, 31)
```

**Impact:**
- Longer period = Better trend analysis
- Longer period = Year-over-year comparisons
- Must be logical (END_DATE > START_DATE)

### Advanced Configuration

#### Random Seed

```python
np.random.seed(42)
random.seed(42)
```

**Purpose:** Reproducibility

**Options:**
- `42` - Default seed (reproducible)
- `None` - Random seed (different data each run)
- Any integer - Custom seed

**When to change:**
```python
# Same data every time (for testing)
np.random.seed(42)

# Different data each time (for variety)
np.random.seed(None)

# Custom seed (for team consistency)
np.random.seed(12345)
```

#### Batch Size

```python
batch_size = 50000  # Process 50K orders at a time
```

**Recommendations:**
- **Low RAM (4GB)**: 25,000
- **Normal RAM (8GB)**: 50,000
- **High RAM (16GB+)**: 100,000

---

## 📊 DATA SCHEMA DESIGN

### Entity-Relationship Diagram

```
┌─────────────────┐
│     USERS       │
│  (Customers)    │
├─────────────────┤
│ PK: user_id     │
│    user_name    │
│    age          │
│    gender       │
│    marital_st.. │
│    occupation   │
└────────┬────────┘
         │
         │ 1:M
         │
         ▼
┌─────────────────┐          ┌─────────────────┐
│     ORDERS      │          │  RESTAURANTS    │
├─────────────────┤          ├─────────────────┤
│ PK: order_id    │          │ PK: restaur...  │
│ FK: user_id     │◄─────────│    restaur...   │
│ FK: restaur...  │    M:1   │    city         │
│    order_date   │          │    cuisine      │
│    delivery...  │          │    rating       │
│    order_sta... │          │    is_cloud...  │
│    payment_...  │          └────────┬────────┘
│    total_amt    │                   │
└────────┬────────┘                   │ 1:M
         │                            │
         │ 1:M                        ▼
         │                   ┌─────────────────┐
         │                   │      MENU       │
         │                   ├─────────────────┤
         │                   │ PK: menu_id     │
         │                   │ FK: restaur...  │
         │                   │    item_name    │
         │                   │    category     │
         │                   │    price        │
         │                   │    is_veg       │
         │                   └────────┬────────┘
         │                            │
         │                            │ M:1
         ▼                            │
┌─────────────────┐                   │
│  ORDER_ITEMS    │                   │
├─────────────────┤                   │
│ PK: order_it... │                   │
│ FK: order_id    │                   │
│ FK: menu_id     │◄──────────────────┘
│    quantity     │
│    price        │
└─────────────────┘
```

### Table Specifications

#### 1. USERS Table

**Purpose:** Customer master data

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `user_id` | VARCHAR(10) | Primary key, format: U00001 | U00542 |
| `user_name` | VARCHAR(100) | Customer full name | Rahul Sharma |
| `age` | INT | Age in years (18-64) | 32 |
| `gender` | VARCHAR(10) | Male or Female | Male |
| `marital_status` | VARCHAR(20) | Single or Married | Married |
| `occupation` | VARCHAR(50) | Job title | Software Engineer |

**Key Constraints:**
- Primary Key: `user_id`
- Check: `age BETWEEN 18 AND 64`
- Check: `gender IN ('Male', 'Female')`
- Check: `marital_status IN ('Single', 'Married')`

**Sample Data:**
```csv
user_id,user_name,age,gender,marital_status,occupation
U00001,Rahul Sharma,32,Male,Married,Software Engineer
U00002,Priya Gupta,28,Female,Single,Marketing Manager
U00003,Amit Singh,45,Male,Married,Doctor
```

#### 2. RESTAURANTS Table

**Purpose:** Restaurant master data

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `restaurant_id` | VARCHAR(10) | Primary key, format: R0001 | R0234 |
| `restaurant_name` | VARCHAR(100) | Restaurant name | Royal Kitchen |
| `city` | VARCHAR(50) | Location city | Mumbai |
| `cuisine` | VARCHAR(50) | Type of cuisine | North Indian |
| `rating` | DECIMAL(2,1) | Rating 0.0-5.0 | 4.5 |
| `is_cloud_kitchen` | TINYINT | 1=Yes, 0=No | 0 |

**Key Constraints:**
- Primary Key: `restaurant_id`
- Check: `rating BETWEEN 0.0 AND 5.0`
- Check: `is_cloud_kitchen IN (0, 1)`

**Sample Data:**
```csv
restaurant_id,restaurant_name,city,cuisine,rating,is_cloud_kitchen
R0001,Royal Kitchen,Mumbai,North Indian,4.5,0
R0002,Spice Corner,Delhi,Chinese,4.2,1
R0003,The Cafe,Bangalore,Continental,4.0,0
```

**City Distribution:**
- Mumbai: 20%
- Delhi: 18%
- Bangalore: 16%
- Hyderabad: 12%
- Chennai: 10%
- Kolkata: 8%
- Pune: 6%
- Ahmedabad: 4%
- Jaipur: 3%
- Lucknow: 3%

**Cuisine Types (20 total):**
```
North Indian, South Indian, Chinese, Italian, Continental,
Fast Food, Biryani, Street Food, Desserts, Beverages,
Mexican, Thai, Japanese, Bakery, Cafe, Healthy Food,
Pizza, Burger, Seafood, Mughlai
```

#### 3. MENU Table

**Purpose:** Menu items for each restaurant

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `menu_id` | VARCHAR(10) | Primary key, format: M000001 | M000542 |
| `restaurant_id` | VARCHAR(10) | Foreign key to restaurants | R0234 |
| `item_name` | VARCHAR(100) | Name of menu item | Butter Chicken |
| `category` | VARCHAR(50) | Item category | Main Course |
| `price` | DECIMAL(10,2) | Price in rupees | 325.50 |
| `is_veg` | TINYINT | 1=Veg, 0=Non-Veg | 0 |

**Key Constraints:**
- Primary Key: `menu_id`
- Foreign Key: `restaurant_id` → `restaurants(restaurant_id)`
- Check: `price > 0`
- Check: `is_veg IN (0, 1)`

**Sample Data:**
```csv
menu_id,restaurant_id,item_name,category,price,is_veg
M000001,R0001,Butter Chicken,Main Course,325.50,0
M000002,R0001,Paneer Tikka,Appetizer,185.00,1
M000003,R0001,Garlic Naan,Rice & Bread,45.00,1
```

**Categories (7 total):**
```
Appetizer, Main Course, Rice & Bread, Pizza, 
Burger, Dessert, Beverage
```

**Menu Items per Restaurant:** 12-25 items (random)

**Price Ranges by Category:**
```
Appetizer:       ₹50 - ₹200
Main Course:     ₹150 - ₹450
Rice & Bread:    ₹50 - ₹200
Pizza:           ₹100 - ₹350
Burger:          ₹100 - ₹350
Dessert:         ₹50 - ₹180
Beverage:        ₹30 - ₹150
```

**Premium Pricing:**
- Restaurants with rating ≥ 4.5 have 20% higher prices

**Vegetarian Status:**
- 82.1% vegetarian items
- 17.9% non-vegetarian items

#### 4. ORDERS Table

**Purpose:** Order transaction records

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `order_id` | VARCHAR(15) | Primary key, format: O0000001 | O0123456 |
| `user_id` | VARCHAR(10) | Foreign key to users | U00542 |
| `restaurant_id` | VARCHAR(10) | Foreign key to restaurants | R0234 |
| `order_date` | DATE | Date of order | 2024-03-15 |
| `delivery_time` | TIME | Time of delivery | 13:45:00 |
| `order_status` | VARCHAR(20) | Delivered or Cancelled | Delivered |
| `payment_method` | VARCHAR(30) | Payment type | UPI |
| `total_amount` | DECIMAL(10,2) | Total order value | 875.50 |

**Key Constraints:**
- Primary Key: `order_id`
- Foreign Keys: `user_id`, `restaurant_id`
- Check: `order_status IN ('Delivered', 'Cancelled')`
- Check: `payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery', 'Wallet')`
- Check: `total_amount >= 0`

**Sample Data:**
```csv
order_id,user_id,restaurant_id,order_date,delivery_time,order_status,payment_method,total_amount
O0000001,U00542,R0234,2024-03-15,13:45:00,Delivered,UPI,875.50
O0000002,U00123,R0567,2024-03-15,19:30:00,Delivered,Credit Card,1250.75
O0000003,U00789,R0089,2024-03-16,12:15:00,Cancelled,Debit Card,0.00
```

**Order Status Distribution:**
- Delivered: 95%
- Cancelled: 5%

**Payment Method Distribution:**
- UPI: 40%
- Credit Card: 25%
- Debit Card: 15%
- Cash on Delivery: 10%
- Wallet: 10%

#### 5. ORDER_ITEMS Table

**Purpose:** Line items for each order

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `order_item_id` | VARCHAR(15) | Primary key, format: OI00000001 | OI00123456 |
| `order_id` | VARCHAR(15) | Foreign key to orders | O0123456 |
| `menu_id` | VARCHAR(10) | Foreign key to menu | M000542 |
| `quantity` | INT | Number of items | 2 |
| `price` | DECIMAL(10,2) | Unit price | 325.50 |

**Key Constraints:**
- Primary Key: `order_item_id`
- Foreign Keys: `order_id`, `menu_id`
- Check: `quantity > 0`
- Check: `price > 0`

**Sample Data:**
```csv
order_item_id,order_id,menu_id,quantity,price
OI00000001,O0000001,M000542,2,325.50
OI00000002,O0000001,M000543,1,185.00
OI00000003,O0000001,M000544,3,45.00
```

**Items per Order Distribution:**
- 1 item: 15%
- 2 items: 30%
- 3 items: 30%
- 4 items: 15%
- 5 items: 7%
- 6 items: 3%

**Quantity Distribution:**
- Quantity 1: 70%
- Quantity 2: 25%
- Quantity 3: 5%

---

## 🧠 GENERATION LOGIC & ALGORITHMS

### 1. User Generation Algorithm

#### Vectorized Implementation

```python
def generate_users(num_users):
    # Pre-generate all arrays at once
    user_ids = [f'U{i:05d}' for i in range(1, num_users + 1)]
    
    user_names = [f"{random.choice(first_names)} {random.choice(last_names)}" 
                  for _ in range(num_users)]
    
    ages = np.random.randint(18, 65, num_users)
    
    genders = np.random.choice(['Male', 'Female'], num_users, p=[0.55, 0.45])
    
    marital_statuses = [
        'Married' if age > 28 and random.random() < 0.6 else 'Single' 
        for age in ages
    ]
    
    occupations_list = [random.choice(occupations) for _ in range(num_users)]
    
    return pd.DataFrame({
        'user_id': user_ids,
        'user_name': user_names,
        'age': ages,
        'gender': genders,
        'marital_status': marital_statuses,
        'occupation': occupations_list
    })
```

**Key Optimizations:**
- List comprehension for IDs (fast)
- NumPy vectorized age generation
- Weighted gender selection
- Age-conditional marital status

### 2. Restaurant Generation Algorithm

```python
def generate_restaurants(num_restaurants):
    # Vectorized city selection with weights
    city_list = np.random.choice(cities, num_restaurants, 
                                  p=[0.20, 0.18, 0.16, 0.12, 0.10, 
                                     0.08, 0.06, 0.04, 0.03, 0.03])
    
    # Realistic rating distribution
    ratings = np.random.choice(
        [3.0, 3.5, 4.0, 4.5, 5.0, 2.5, 3.2, 3.8, 4.2, 4.7],
        num_restaurants,
        p=[0.05, 0.15, 0.25, 0.30, 0.10, 0.03, 0.04, 0.03, 0.03, 0.02]
    )
    
    # Cloud kitchen split
    is_cloud_kitchen = np.random.choice([0, 1], num_restaurants, p=[0.7, 0.3])
    
    # ... create DataFrame
```

**Rating Distribution:**
- Most ratings (30%) at 4.5
- Bell curve around 3.5-4.5
- Few poor ratings (<3.0)

### 3. Menu Generation with is_veg

```python
# Define vegetarian items
veg_items = {
    'Paneer Tikka', 'French Fries', 'Dal Makhani', 
    'Veg Biryani', 'Margherita Pizza', ...
}

# Classification logic
if item in ['Spring Rolls', 'Momos']:
    is_veg = random.choice([0, 1])  # Ambiguous items
elif item in veg_items:
    is_veg = 1
else:
    is_veg = 0
```

**Set-Based Duplicate Prevention:**
```python
selected = set()  # O(1) lookup

for _ in range(num_items):
    category = random.choice(list(menu_items.keys()))
    item = random.choice(menu_items[category])
    
    if (category, item) in selected:
        continue
    
    selected.add((category, item))
```

### 4. Orders Generation (Vectorized)

#### 80-20 Rule Implementation

```python
# Pre-calculate user arrays
user_ids = users_df['user_id'].values
heavy_users = np.random.choice(user_ids, int(len(user_ids) * 0.2), 
                               replace=False)

# Vectorized user selection (600K at once)
user_selection = np.random.rand(num_orders)

selected_users = np.where(
    user_selection < 0.8,
    np.random.choice(heavy_users, num_orders),
    np.random.choice(user_ids, num_orders)
)
```

#### Peak Hours (Nested np.where)

```python
hour_probs = np.random.rand(num_orders)

hours = np.where(
    hour_probs < 0.4,                        # 40% lunch
    np.random.randint(12, 15, num_orders),
    np.where(
        hour_probs < 0.75,                   # 35% dinner
        np.random.randint(19, 23, num_orders),
        np.random.randint(8, 24, num_orders) # 25% other
    )
)
```

### 5. Order Items with Total Calculation

#### Menu Grouping (O(1) Lookup)

```python
# Pre-group menu by restaurant
menu_by_restaurant = {k: v for k, v in menu_df.groupby('restaurant_id')}

# Fast lookup during order item generation
restaurant_menu = menu_by_restaurant[restaurant_id]  # Instant!
```

#### Batch Processing

```python
batch_size = 50000
total_batches = (len(orders_df) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(orders_df))
    
    # Progress indicator
    if batch_num % 5 == 0:
        print(f"  Processing batch {batch_num + 1}/{total_batches}...", 
              end='\r')
    
    # Process this batch
    for idx in range(start_idx, end_idx):
        # ... generate order items
```

---

## 🎯 REALISTIC PATTERNS IMPLEMENTATION

### 1. Pareto Principle (80-20 Rule)

**Implementation:**
```python
heavy_users = random.sample(user_ids, int(len(user_ids) * 0.2))

for order in orders:
    if random.random() < 0.8:
        user = random.choice(heavy_users)
    else:
        user = random.choice(all_users)
```

**Result:** 20% of users make 80% of orders

### 2. Peak Hour Distribution

**Distribution:**
- Lunch (12-2 PM): 40% of orders
- Dinner (7-10 PM): 35% of orders
- Other times: 25% of orders

### 3. Weekend Surge

**Result:** ~35% more orders on weekends

### 4. Age-Based Marital Status

**Logic:**
- Age 18-28: 25% married
- Age 29-64: 60% married

### 5. Premium Pricing

**Implementation:**
```python
if restaurant['rating'] >= 4.5:
    price *= 1.2  # 20% premium
```

### 6. Payment Method Preference

**Distribution:**
- UPI: 40%
- Credit Card: 25%
- Debit Card: 15%
- COD: 10%
- Wallet: 10%

### 7. Vegetarian Preference

**Result:** 82.1% vegetarian menu items (reflects Indian market)

---

## ✅ DATA QUALITY & VALIDATION

### Built-in Validations

```python
# 1. Referential integrity
assert all(orders_df['user_id'].isin(users_df['user_id']))
assert all(orders_df['restaurant_id'].isin(restaurants_df['restaurant_id']))

# 2. No missing values
assert users_df.isnull().sum().sum() == 0

# 3. No duplicates
assert len(users_df) == users_df['user_id'].nunique()

# 4. Value ranges
assert (users_df['age'] >= 18).all() and (users_df['age'] <= 64).all()
assert (restaurants_df['rating'] >= 0).all() and (restaurants_df['rating'] <= 5).all()
```

### SQL Validation Queries

```sql
-- Check for orphaned records
SELECT 'Orders without users' as check_type, COUNT(*) as count
FROM orders o
LEFT JOIN users u ON o.user_id = u.user_id
WHERE u.user_id IS NULL;

-- Validate total amounts
SELECT 
    o.order_id,
    o.total_amount as order_total,
    SUM(oi.quantity * oi.price) as calculated_total,
    ABS(o.total_amount - SUM(oi.quantity * oi.price)) as difference
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.total_amount
HAVING difference > 0.01;
```

---

## ⚡ PERFORMANCE OPTIMIZATION

### Optimization Techniques

#### 1. Vectorization with NumPy

**Before:**
```python
ages = []
for i in range(10000):
    ages.append(random.randint(18, 64))
```

**After:**
```python
ages = np.random.randint(18, 65, 10000)
```

**Speedup:** 100x-1000x

#### 2. DataFrame Direct Creation

**Before:**
```python
df = pd.DataFrame()
for user in users:
    df = df.append(user, ignore_index=True)  # O(n²)
```

**After:**
```python
df = pd.DataFrame({
    'user_id': user_ids,
    'user_name': user_names,
    ...
})  # O(n)
```

**Speedup:** 1000x+

#### 3. Dictionary Lookup vs Filtering

**Before:**
```python
for order in orders:
    menu = menu_df[menu_df['restaurant_id'] == rid]  # O(n)
```

**After:**
```python
menu_by_restaurant = {k: v for k, v in menu_df.groupby('restaurant_id')}
for order in orders:
    menu = menu_by_restaurant[rid]  # O(1)
```

**Speedup:** 100x-500x

### Performance Benchmarks

| Operation | Records | Loop Time | Optimized Time | Speedup |
|-----------|---------|-----------|----------------|---------|
| Users | 10,000 | 2.5s | 0.1s | 25x |
| Restaurants | 1,000 | 0.5s | 0.05s | 10x |
| Menu | 15,000 | 15s | 1.5s | 10x |
| Orders | 600,000 | 8 min | 30s | 16x |
| Order Items | 1.67M | 15 min | 60s | 15x |
| **Total** | - | ~25 min | ~2 min | **12x** |

---

## 🔧 TROUBLESHOOTING

### Common Issues

#### Issue 1: Script Takes Too Long

**Solutions:**
```python
# Reduce dataset size
NUM_ORDERS = 100000

# Increase batch size
batch_size = 100000
```

#### Issue 2: Memory Error

**Solutions:**
```python
# Reduce batch size
batch_size = 25000

# Process in chunks
for i in range(6):
    generate_orders_batch(100000)
```

#### Issue 3: CSV Files Not Created

**Solutions:**
```bash
# Check permissions
chmod 755 /output/directory/

# Use absolute paths
output_dir = '/full/path/to/output/'
```

#### Issue 4: Import Errors

**Solutions:**
```bash
pip install pandas numpy
python --version  # Check 3.8+
```

---

## 🎨 ADVANCED CUSTOMIZATION

### Adding New Cities

```python
cities = [
    'Mumbai', 'Delhi', 'Bangalore', ...,
    'Surat', 'Kanpur', 'Nagpur'  # Add new cities
]

probabilities = [
    0.18, 0.16, 0.14, ...,
    0.04, 0.03, 0.03  # Update probabilities (must sum to 1.0)
]
```

### Adding New Menu Items

```python
menu_items = {
    'Appetizer': [
        'Spring Rolls', 'Paneer Tikka', ...,
        'Hummus', 'Falafel', 'Bruschetta'  # Add new items
    ],
    'Soup': ['Tomato Soup', 'Hot and Sour Soup'],  # New category
}

veg_items = {
    # ... existing items
    'Hummus', 'Falafel', 'Bruschetta'  # Update veg items
}
```

### Changing Distributions

```python
# Modify peak hours (30% lunch, 50% dinner)
hours = np.where(
    hour_probs < 0.3,
    np.random.randint(12, 15, num_orders),
    np.where(
        hour_probs < 0.8,
        np.random.randint(19, 23, num_orders),
        np.random.randint(8, 24, num_orders)
    )
)

# Modify payment distribution
payment_methods = np.random.choice(
    ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery', 'Wallet'],
    num_orders,
    p=[0.30, 0.20, 0.45, 0.02, 0.03]  # New distribution
)
```

### Adding Seasonal Patterns

```python
def generate_orders_with_seasonality(...):
    for i in range(num_orders):
        order_date = start_date + timedelta(days=random_day)
        month = order_date.month
        
        # More orders during festivals (Oct-Dec)
        if month in [10, 11, 12]:
            if random.random() > 0.3:
                continue
        
        # Fewer orders during summer (Apr-Jun)
        elif month in [4, 5, 6]:
            if random.random() > 0.5:
                random_day = random.randint(0, days_diff)
                order_date = start_date + timedelta(days=random_day)
```

---

## ❓ FAQs

### General Questions

**Q1: How long does it take to generate 600K orders?**

A: Approximately 30-60 seconds on a modern computer.

**Q2: Can I generate more than 1 million orders?**

A: Yes, but expect 2-3 minutes generation time and higher memory usage.

**Q3: Why use random seeds?**

A: Seeds ensure reproducibility - same seed = same data every time.

**Q4: Can I use this data commercially?**

A: Yes, this is synthetic data you generated.

**Q5: How do I import into MySQL?**

```sql
LOAD DATA LOCAL INFILE 'users.csv' 
INTO TABLE users 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;
```

### Technical Questions

**Q6: Why NumPy instead of loops?**

A: NumPy is 10-100x faster (C implementation) and more memory efficient.

**Q7: How much disk space needed?**

A:
- 100K orders: ~20 MB
- 600K orders: ~130 MB
- 1M orders: ~220 MB

**Q8: Can I modify for my use case?**

A: Absolutely! See Advanced Customization section.

### Customization Questions

**Q9: Can I add delivery charges?**

```python
orders_df['delivery_fee'] = np.random.choice(
    [0, 20, 40, 60], 
    num_orders, 
    p=[0.3, 0.4, 0.2, 0.1]
)
```

**Q10: Can I add customer ratings?**

```python
orders_df['customer_rating'] = np.random.choice(
    [1, 2, 3, 4, 5], 
    num_orders, 
    p=[0.02, 0.03, 0.10, 0.35, 0.50]
)
```

---

## 📚 ADDITIONAL RESOURCES

### Related Documentation

- **PROJECT_DOCUMENTATION.md** - Complete project guide
- **BUSINESS_PROBLEMS.md** - Analysis approaches
- **schema_creation.sql** - Database schema
- **analysis_queries.sql** - SQL queries
- **vegetarian_analysis_queries.sql** - Veg-specific queries

### Python Libraries

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Python Random Module](https://docs.python.org/3/library/random.html)

---

## 📝 VERSION HISTORY

### Version 2.0 (Current)
- Added `is_veg` column
- Increased to 600K orders
- Extended to 4 years
- Optimized generation speed
- Added batch processing

### Version 1.0
- Initial release
- 100K orders
- 2 years of data

---

## 🤝 SUPPORT

For issues:
1. Check Troubleshooting section
2. Review FAQs
3. Validate data using provided scripts
4. Check Python/library versions

---

## 📄 LICENSE

This data generation script is provided for educational and portfolio purposes.

---

# ⚠️ Dataset Disclaimer  

All datasets used are **dummy, synthetic, or public**, intended only for learning and portfolio demonstration.  
No real customer or company data is used.

**Last Updated:** February 2026  
**Version:** 2.0

---

## 🧑‍💻 Author

**👤 Harsh Belekar**  
📍 Data Analyst | Python Developer | SQL | Power BI | Excel | Data Visualization  
📬 [LinkedIn](https://www.linkedin.com/in/harshbelekar) | 🔗[GitHub](https://github.com/Harsh-Belekar)

📧 [harshbelekar74@gmail.com](mailto:harshbelekar74@gmail.com)

---

⭐ *If you found this project helpful, feel free to star the repo and connect with me for collaboration!*

**Happy Data Generating! 🚀**
