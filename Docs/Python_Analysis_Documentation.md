# 🍔 Swiggy Sales Analysis — Python Analysis Documentation

> **Notebook:** `Swiggy_Data_Analysis.ipynb`
> **Data Period:** 2022 – 2025 (4 Years)
> **Analyst Reference:** Step-by-Step guide explaining every analysis performed to solve 7 critical business challenges.

---

## 📑 Table of Contents

1. [Project Overview](#1️⃣-project-overview)
2. [Setup & Data Loading](#2️⃣-️setup--data-loading)
3. [Customer Retention & Engagement Analysis](#3️⃣-customer-retention--engagement-analysis)
   - [3.1 Customer Type Distribution](#31-customer-type-distribution)
   - [3.2 Cohort Retention Rate Analysis](#32-cohort-retention-rate-analysis)
   - [3.3 Customer Lifetime Value (CLV)](#33-customer-lifetime-value-clv-analysis)
   - [3.4 RFM Segmentation](#34-rfm-recency-frequency-monetary-segmentation)
   - [3.5 Churn Risk Analysis](#35-churn-risk-analysis)
   - [3.6 Customer Behavior by Demographics](#36-customer-behavior-by-demographics)
4. [Revenue Optimization Analysis](#4️⃣-revenue-optimization-analysis)
   - [4.1 Yearly Revenue Trend](#41-yearly-revenue-trend)
   - [4.2 Monthly & Quarterly Revenue](#42-monthly--quarterly-revenue)
   - [4.3 Revenue Drivers — City, Cuisine, Time](#43-revenue-drivers--city-cuisine-time)
   - [4.4 Average Order Value (AOV) Analysis](#44-average-order-value-aov-analysis)
   - [4.5 Seasonal Patterns](#45-seasonal-patterns)
5. [Restaurant Partner Performance Analysis](#5️⃣-restaurant-partner-performance-analysis)
   - [5.1 Top & Bottom Restaurant Revenue](#51-top--bottom-restaurant-revenue)
   - [5.2 Rating Impact Analysis](#52-rating-impact-analysis)
   - [5.3 Cloud Kitchen vs Traditional](#53-cloud-kitchen-vs-traditional-performance)
   - [5.4 Cuisine Performance by City](#54-cuisine-performance-by-city)
   - [5.5 Restaurant Efficiency & Underperformers](#55-restaurant-efficiency--underperformers)
6. [Menu & Product Optimization](#6️⃣-️menu--product-optimization)
   - [6.1 Best-Selling Items](#61-best-selling-items-analysis)
   - [6.2 Veg vs Non-Veg Analysis](#62-veg-vs-non-veg-analysis)
   - [6.3 Price Category Analysis](#63-price-category-analysis)
   - [6.4 Basket Analysis](#64-basket-analysis-items-ordered-together)
   - [6.5 Revenue & Margin by Category](#65-revenue--margin-analysis-by-category)
7. [Operational Efficiency Analysis](#7️⃣-operational-efficiency-analysis)
   - [7.1 Order Distribution Patterns](#71-order-distribution-patterns)
   - [7.2 Peak Hours & Capacity Analysis](#72-peak-hours--capacity-analysis)
   - [7.3 Cancellation Analysis](#73-cancellation-analysis)
   - [7.4 Weekend vs Weekday Demand](#74-weekend-vs-weekday-demand)
8. [Market Expansion & Growth Analysis](#8️⃣-market-expansion--growth-analysis)
   - [8.1 City Performance Metrics](#81-city-performance-metrics)
   - [8.2 Market Saturation Analysis](#82-market-saturation-analysis)
   - [8.3 Cuisine Gap Analysis](#83-cuisine-gap-analysis)
   - [8.4 Market Penetration Analysis](#84-market-penetration-analysis)
   - [8.5 Final Expansion Recommendation](#85-final-expansion-recommendation)
9. [Customer Experience Analysis](#9️⃣-customer-experience-analysis)
   - [9.1 Payment Method Analysis](#91-payment-method-analysis)
   - [9.2 Demographic Behavior Patterns](#92-demographic-behavior-patterns)
   - [9.3 Order Value Influencers](#93-order-value-influencers)
   - [9.4 Customer Journey — First vs Repeat Orders](#94-customer-journey--first-vs-repeat-orders)
   - [9.5 Satisfaction Proxies](#95-satisfaction-proxies)
10. [Statistical Significance & Revenue Forecasting](#-statistical-significance--revenue-forecasting)
11. [Strategic Recommendations](#1️⃣1️⃣-strategic-recommendations)
12. [Executive Summary](#1️⃣2️⃣-executive-summary)
13. [Author](#-author)

---

## 1️⃣. 📋Project Overview 

### 🎯 Business Context

Swiggy is one of India's leading food delivery platforms. Despite achieving strong revenue, the company faces critical challenges across customer retention, revenue growth, restaurant performance, and operational efficiency. This analysis uses **600,000+ orders** across **10 cities** and **4 years (2022–2025)** to produce data-driven solutions for **7 key business problems**.

### 📊 Key Platform Metrics

| Metric | Value |
|---|---|
| Total Gross Order Value | ₹39.62 Crores |
| Total Orders Processed | 6,00,000 |
| Active Customers | 10,000+ |
| Restaurant Partners | 1,000 |
| Cities Covered | 10 |
| Order Fulfillment Rate | 95% |
| Order Cancellation Rate | ~5% |

### 🔴 7 Business Challenges Addressed

| # | Business Challenge |
|---|---|
| 1 | Customer Retention & Engagement |
| 2 | Revenue Optimization |
| 3 | Restaurant Partner Performance |
| 4 | Menu & Product Optimization |
| 5 | Operational Efficiency |
| 6 | Market Expansion & Growth |
| 7 | Customer Experience & Satisfaction |

---

## 2️⃣. ⚙️Setup & Data Loading

### 2.1 Library Imports & Global Settings

The first step is importing all required Python libraries and configuring the display and plotting environment.

```python
# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.expand_frame_repr', False)

# Set plotting style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("Libraries imported successfully")
```

**Why this matters:** Setting display options upfront ensures that all DataFrames print without truncation, currency values show two decimal places, and all charts maintain a consistent `whitegrid` style throughout the notebook.

---

### 2.2 Database Connection

The data is stored in a **PostgreSQL** database. We connect to it using `SQLAlchemy`'s `create_engine`.

```python
# Database Connection
engine = create_engine(
    "postgresql+psycopg2://postgres:your_password@localhost:5432/swiggy"
)

print("Database connection established")
```

> **Note for other analysts:** Replace `your_password` with your own PostgreSQL password before running.

---

### 2.3 Loading Data from PostgreSQL

Two master tables are loaded from the database:

| Table | Description |
|---|---|
| `orders_master` | One row per order — customer, restaurant, location, time, amount, status |
| `order_items_master` | One row per item in each order — item name, category, price, type (Veg/Non-Veg) |

```python
# Load Aggregated Tables from PostgreSQL
orders_master = pd.read_sql("SELECT * FROM orders_master", engine)
order_items_master = pd.read_sql("SELECT * FROM order_items_master", engine)

# Convert data types
orders_master['order_date'] = pd.to_datetime(orders_master['order_date'])
orders_master['rating_bucket'] = orders_master['rating_bucket'].astype('category')
orders_master['order_year']    = orders_master['order_year'].astype('int')
orders_master['order_month']   = orders_master['order_month'].astype('int')
orders_master['order_quarter'] = orders_master['order_quarter'].astype('int')
orders_master['day_of_week']   = orders_master['day_of_week'].astype('int')
```

After loading, data types are explicitly corrected so that date arithmetic, category grouping, and integer-based filtering all work correctly.

---

### 2.4 Data Quality Checks

Before any analysis, a quick quality audit confirms the data is clean and trustworthy.

```python
# Check for duplicates
print(f"Duplicate orders: {orders_master['order_id'].duplicated().sum()}")
print(f"Duplicate order item ids: {order_items_master['order_item_id'].duplicated().sum()}")

# Check date ranges
print(f"Date range: {orders_master['order_date'].min()} to {orders_master['order_date'].max()}")

# Check for missing values in key fields
print(orders_master[['order_id', 'user_id', 'restaurant_id', 'total_amount']].isnull().sum())
```

✅ No duplicates found. No missing values in key columns. Date range confirmed as 2022–2025.

---

### 2.5 Data Overview (Key Business Metrics Snapshot)

```python
delivered = orders_master[orders_master['order_status'] == 'Delivered']

total_orders       = len(orders_master)
total_revenue      = delivered['total_amount'].sum()
avg_order_value    = delivered['total_amount'].mean()
total_customers    = orders_master['user_id'].nunique()
total_restaurants  = orders_master['restaurant_id'].nunique()
delivered_orders   = (orders_master['order_status'] == 'Delivered').sum()
cancelled_orders   = (orders_master['order_status'] == 'Cancelled').sum()
cancellation_rate  = (cancelled_orders / total_orders) * 100
```

**Output:**

| Metric | Value |
|---|---|
| Total Orders | 6,00,000 |
| Total Revenue | ₹39,62,12,XXX (₹39.62 Crores) |
| Average Order Value | ₹695 |
| Unique Customers | 10,000 |
| Unique Restaurants | 1,000 |
| Delivered Orders | 5,70,281 (95.0%) |
| Cancelled Orders | 29,719 (4.95%) |

### 💡 Key Insights from Data Overview

- **Robust Revenue Growth:** ₹39.62 Crores in Gross Order Value demonstrates a strong, scaling market presence.
- **High Operational Reliability:** 95% fulfillment rate confirms a stable delivery network.
- **High Customer Stickiness:** An average of 60 orders per customer signals deep platform integration.
- **Revenue Leakage Alert:** The 5% cancellation rate accounts for ~29,719 orders. Reducing this by even 1% could recover approximately ₹40 Lakhs in GOV.

---

## 3️⃣. 👥Customer Retention & Engagement Analysis

> **Business Challenge #1 — Questions Answered:**
> - What is our customer retention rate?
> - Who are our most valuable customers?
> - How can we identify customers at risk of churning?
> - What drives customer loyalty?
> - Which customer segments should we prioritize?

All customer analysis is performed on **delivered orders only** to avoid counting cancelled transactions.

```python
delivered_orders = orders_master[orders_master['order_status'] == 'Delivered'].copy()
```

---

### 3.1 Customer Type Distribution

**Goal:** Classify every customer into a loyalty tier based on how many times they have ordered.

```python
# Calculate Customer Order Frequency
customer_orders = delivered_orders.groupby('user_id').agg({
    'order_id': 'count',
    'total_amount': 'sum',
    'order_date': ['min', 'max']
}).reset_index()

customer_orders.columns = ['user_id', 'total_orders', 'total_spent', 'first_order', 'last_order']

# Classify customers
customer_orders['customer_type'] = pd.cut(
    customer_orders['total_orders'],
    bins=[0, 1, 5, 15, np.inf],
    labels=['One-Time', 'Occasional', 'Regular', 'Loyal']
)
```

**Classification Logic:**

| Customer Type | Order Count Range |
|---|---|
| One-Time | 1 order |
| Occasional | 2 – 5 orders |
| Regular | 6 – 15 orders |
| Loyal | 16+ orders |

**Output:**

| Customer Type | Count | Percentage |
|---|---|---|
| One-Time | 0 | 0.0% |
| Occasional | ~240 | 2.4% |
| Regular | ~6,830 | 68.3% |
| Loyal | ~2,940 | 29.4% |

**📊 Chart:**

![Customer Type Distribution](../Visuals/customer_type_distribution.png)

>*The chart shows a Pie chart (left) and a Bar chart (right) — both displaying the proportion of customers in each loyalty tier.*

### 💡 Key Insights

- **Elite Retention Levels:** With 0% one-time customers, Swiggy has achieved "habitual" status where every user returns.
- **Core Revenue Engine:** Regular (68.3%) and Loyal (29.4%) segments represent 97.7% of the total base, creating a highly predictable revenue stream.
- **High-Growth Pivot:** Moving the 2.4% Occasional users into the "Regular" tier is the final step toward a 100% high-frequency ecosystem.

---

### 3.2 Cohort Retention Rate Analysis

**Goal:** Understand what percentage of customers from each monthly cohort return in subsequent months.

**Step 1 — Assign each customer their cohort (month of first order):**

```python
delivered_orders['order_month_year'] = delivered_orders['order_date'].dt.to_period('M')
delivered_orders['cohort'] = delivered_orders.groupby('user_id')['order_date'].transform('min').dt.to_period('M')
delivered_orders['cohort_age'] = (delivered_orders['order_month_year'] - delivered_orders['cohort']).apply(lambda x: x.n)
```

**Step 2 — Build the cohort matrix:**

```python
cohort_data   = delivered_orders.groupby(['cohort', 'cohort_age'])['user_id'].nunique().reset_index()
cohort_matrix = cohort_data.pivot(index='cohort', columns='cohort_age', values='customers')

# Calculate retention rate
cohort_size      = cohort_matrix.iloc[:, 0]
retention_matrix = cohort_matrix.divide(cohort_size, axis=0) * 100
```

**Output — Key Retention Metrics:**

| Metric | Value |
|---|---|
| Month 1 Retention Rate | ~26.0% |
| Month 3 Retention Rate | ~24.0% |
| Month 6 Retention Rate | ~24.0% |

### 💡 Key Insights

- **The "Retention Cliff":** ~74% of users are lost after Month 1. The business is currently in a "High-Acquisition, High-Churn" cycle.
- **Stabilization Point:** Retention plateaus at ~24% from Month 3 onwards — if a user survives the first 90 days, they become a permanent "Regular."
- **Below Industry Benchmark:** The 26% Month 1 rate sits 10–15% below industry leaders, indicating a gap in product-market fit or service quality.
- **The January 2022 Anomaly:** The Jan-2022 cohort shows 60%+ retention vs. 22.9% in Feb-2022 — likely due to organic high-intent early adopters vs. later discount hunters.

---

### 3.3 Customer Lifetime Value (CLV) Analysis

**Goal:** Estimate the projected 3-year financial value of each customer and understand the economic difference between loyalty tiers.

**Step 1 — Calculate CLV Metrics:**

```python
customer_orders['avg_order_value']       = customer_orders['total_spent'] / customer_orders['total_orders']
customer_orders['customer_lifetime_days'] = (customer_orders['last_order'] - customer_orders['first_order']).dt.days
customer_orders['orders_per_year']       = np.where(
    customer_orders['customer_lifetime_days'] > 0,
    customer_orders['total_orders'] / (customer_orders['customer_lifetime_days'] / 365),
    customer_orders['total_orders']
)

# 3-Year CLV Projection
customer_orders['estimated_clv_3yr'] = customer_orders['avg_order_value'] * customer_orders['orders_per_year'] * 3
```

**Output — CLV Summary:**

| Metric | Value |
|---|---|
| Average CLV (3-year) | ~₹ (varies by segment) |
| Loyal Customer CLV | ~₹88,972 |
| Occasional Customer CLV | ~₹3,998 |
| CLV Multiplier | **22x** |

**Step 2 — Pareto Analysis (80-20 Rule):**

```python
customer_orders_sorted = customer_orders.sort_values('total_spent', ascending=False)
customer_orders_sorted['cumulative_revenue']     = customer_orders_sorted['total_spent'].cumsum()
customer_orders_sorted['cumulative_revenue_pct'] = (customer_orders_sorted['cumulative_revenue'] / customer_orders_sorted['total_spent'].sum()) * 100
customer_orders_sorted['customer_rank_pct']      = (customer_orders_sorted.reset_index(drop=True).index + 1) / len(customer_orders_sorted) * 100

top_20_pct_customers    = customer_orders_sorted[customer_orders_sorted['customer_rank_pct'] <= 20]
revenue_pct_from_top_20 = (top_20_pct_customers['total_spent'].sum() / customer_orders_sorted['total_spent'].sum()) * 100
```

**Output:**

| Metric | Value |
|---|---|
| Top 20% customers | ~2,000 |
| Revenue from Top 20% | **84.1%** |
| Average spend (Top 20%) | Much higher |
| Average spend (Bottom 80%) | Much lower |

**📊 Chart:**

![CLV by Customer Type and Pareto Chart](../Visuals/clv_pareto_analysis.png)

>*Left: Bar chart of Average 3-Year CLV by customer type. Right: Pareto Curve showing cumulative revenue contribution by customer percentage.*

### 💡 Key Insights

- **Extreme Revenue Concentration:** The Top 20% of users drive 84.1% of total revenue — Swiggy is a "whale-driven" business.
- **The Loyalty Multiplier:** Loyal customers have a CLV 22x higher than Occasional users, quantifying the massive ROI of retention over acquisition.
- **Protection Strategy:** A 1% churn in the "Loyal" segment is more damaging than a 20% churn in "Occasional" users.

---

### 3.4 RFM (Recency, Frequency, Monetary) Segmentation

**Goal:** Score every customer on three dimensions and assign them to strategic business segments for targeted action.

**What is RFM?**
- **Recency (R):** How many days since the customer last ordered? *(Lower = Better)*
- **Frequency (F):** How many total orders has the customer placed? *(Higher = Better)*
- **Monetary (M):** How much total money has the customer spent? *(Higher = Better)*

**Step 1 — Calculate RFM Metrics:**

```python
analysis_date = delivered_orders['order_date'].max() + timedelta(days=1)

rfm = delivered_orders.groupby('user_id').agg({
    'order_date':    lambda x: (analysis_date - x.max()).days,  # Recency
    'order_id':      'count',                                    # Frequency
    'total_amount':  'sum'                                       # Monetary
}).reset_index()

rfm.columns = ['user_id', 'recency', 'frequency', 'monetary']
```

**Step 2 — Assign Quintile Scores (1–5):**

```python
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])        # Lower recency = Score 5
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'),  5, labels=[1, 2, 3, 4, 5])

rfm['r_score'] = rfm['r_score'].astype(int)
rfm['f_score'] = rfm['f_score'].astype(int)
rfm['m_score'] = rfm['m_score'].astype(int)

rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']
```

**Step 3 — Segment Customers by RFM Score:**

```python
def segment_customer(row):
    if row['rfm_score'] >= 13:
        return 'Champions'
    elif row['rfm_score'] >= 11:
        return 'Loyal Customers'
    elif row['rfm_score'] >= 9 and row['r_score'] >= 4:
        return 'Potential Loyalists'
    elif row['rfm_score'] >= 9:
        return 'Recent Customers'
    elif row['rfm_score'] >= 7 and row['f_score'] >= 3:
        return 'Promising'
    elif row['rfm_score'] >= 7:
        return 'Need Attention'
    elif row['rfm_score'] >= 5 and row['r_score'] <= 2:
        return 'At Risk'
    elif row['r_score'] <= 2:
        return 'Lost Customers'
    else:
        return 'Hibernating'

rfm['segment'] = rfm.apply(segment_customer, axis=1)
```

**Segment Logic Table:**

| Segment | RFM Score Rule | Business Meaning |
|---|---|---|
| Champions | ≥ 13 | Best customers — recent, frequent, high-value |
| Loyal Customers | ≥ 11 | High-value but slightly less recent |
| Potential Loyalists | ≥ 9, R ≥ 4 | Recent but low frequency — great growth potential |
| Recent Customers | ≥ 9 | New but promising |
| Promising | ≥ 7, F ≥ 3 | Moderate engagement |
| Need Attention | ≥ 7 | Losing momentum |
| At Risk | ≥ 5, R ≤ 2 | Haven't ordered in a long time |
| Lost Customers | R ≤ 2 | Effectively churned |
| Hibernating | All others | Very low activity |

**Output — RFM Segment Summary:**

| Segment | Customers | Avg Recency (days) | Avg Frequency | Avg Monetary (₹) |
|---|---|---|---|---|
| Champions | 2,138 (21.4%) | Recent | 225+ orders | High |
| Loyal Customers | — | — | — | — |
| At Risk | 1,075 | ~213 days | Low | ~₹6,800 |
| Hibernating | ~12% | ~282 days | Low | ~₹4,624 |

**📊 Charts:**

![RFM Segment Volume vs Revenue](../Visuals/rfm_segment_volume_revenue.png)

>*Left: Horizontal bar chart of customer count per segment. Right: Horizontal bar chart of total revenue per segment.*

![RFM Score Distribution and Segment Pie](../Visuals/rfm_score_distribution_pie.png)

>*Left: Histogram of RFM scores with average score line. Right: Donut pie chart showing segment percentage distribution.*

### 💡 Key Insights

- **"Super-User" Tier:** Champions (21.4%) order 14.5x more frequently than Loyalists — they are the backbone of ₹33.4 Cr revenue.
- **Impending Revenue Leak:** 1,075 "At Risk" users haven't ordered in 213 days, representing a potential loss of ~₹6,800 per head.
- **Lifecycle Triggers Needed:** Set 30/60/90-day automated re-engagement triggers for "Need Attention" and "Potential Loyalists" to prevent them from sliding toward "Hibernating."

---

### 3.5 Churn Risk Analysis

**Goal:** Quantify the revenue at stake from inactive customers.

```python
# At-Risk: 90+ days without an order
at_risk_customers = rfm[rfm['recency'] > 90].copy()
lost_customers    = rfm[rfm['recency'] > 180].copy()

at_risk_revenue = at_risk_customers['monetary'].sum()
lost_revenue    = lost_customers['monetary'].sum()
```

**Output:**

| Metric | Value |
|---|---|
| At-Risk Customers (90+ days) | 3,892 (38.9%) |
| Revenue at Risk | ₹2.87 Crores |
| Lost Customers (180+ days) | ~1,900 (19%) |
| Lost Revenue | ₹1.29 Crores |

### 💡 Key Insights

- **₹2.87 Crores at Stake:** Nearly 39% of customers haven't ordered in 90+ days.
- **The "Point of No Return":** Customers crossing the 180-day mark have a very low return probability.
- **Escalated Recovery Ladder:**
  - 45 days → Soft re-engagement notification
  - 60 days → High-value coupon offer
  - 90+ days → Direct feedback survey to identify churn reason

---

### 3.6 Customer Behavior by Demographics

**Goal:** Understand how age group, gender, and occupation influence ordering behaviour and revenue.

**Step 1 — Merge RFM segments with order data:**

```python
orders_with_rfm = delivered_orders.merge(rfm[['user_id', 'segment']], on='user_id', how='left')
```

**Step 2 — Age Group Analysis:**

```python
age_analysis = orders_with_rfm.groupby('age_group').agg({
    'user_id':      'nunique',
    'order_id':     'count',
    'total_amount': ['mean', 'sum']
}).round(2)
```

**Step 3 — Gender Analysis:**

```python
gender_analysis = orders_with_rfm.groupby('gender').agg({
    'user_id':      'nunique',
    'order_id':     'count',
    'total_amount': ['mean', 'sum']
}).round(2)
```

**Step 4 — Occupation Analysis (Top 10 by Revenue):**

```python
occupation_analysis = orders_with_rfm.groupby('occupation').agg({
    'user_id':      'nunique',
    'total_amount': ['mean', 'sum']
}).round(2)

occupation_analysis = occupation_analysis.sort_values('Total_Revenue', ascending=False).head(10)
```

**📊 Charts:**

![Age Group Orders and AOV](../Visuals/age_group_orders_aov.png)

>*Left: Bar chart of total orders by age group. Right: Bar chart of Average Order Value by age group.*

![Revenue by Gender and Occupation](../Visuals/gender_occupation_revenue.png)

>*Left: Bar chart of total revenue by gender. Right: Horizontal bar chart of top 10 occupations by revenue.*

### 💡 Key Insights

- **The "Prime Spenders":** The 26–35 age group is the largest revenue contributor (₹8.86 Cr) due to high-income urban professionals.
- **High-Tech Dominance:** Software Engineers and Data Analysts lead revenue charts — "desk-bound" professionals are highest-value due to frequency.
- **Balanced Gender Reach:** Revenue is split ~54% Male / 46% Female, showing universal platform utility.
- **Corporate Opportunity:** Since Tech and Finance professionals dominate, Swiggy should launch Corporate Subscription Plans (e.g., "Swiggy for Business") for major IT hubs.

---


## 4️⃣. 💰Revenue Optimization Analysis

> **Business Challenge #2 — Questions Answered:**
> - What are the key revenue drivers?
> - Which months/quarters show the highest revenue?
> - What is the year-over-year growth rate?
> - How does AOV vary across segments?
> - What pricing strategies can maximize revenue?

---

### 4.1 Yearly Revenue Trend

**Goal:** Calculate total revenue and year-over-year growth for each year.

```python
revenue_summary = delivered_orders.groupby('order_year').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

revenue_summary.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value']
revenue_summary['YoY_Growth_(%)'] = revenue_summary['Total_Revenue'].pct_change() * 100
```

**Output:**

| Year | Orders | Total Revenue | Avg Order Value | YoY Growth |
|---|---|---|---|---|
| 2022 | ~1.4L | ~₹9.84 Cr | ~₹695 | — |
| 2023 | ~1.4L | ~₹9.86 Cr | ~₹696 | +0.2% |
| 2024 | ~1.4L | ~₹9.96 Cr | ~₹697 | +1.01% |
| 2025 | ~1.4L | ~₹9.90 Cr | ~₹696 | -0.58% |

### 💡 Key Insights

- **Growth Stagnation:** 0.15% average annual growth rate — revenue is stable but strictly horizontal.
- **Marginal 2024 Peak:** 2024 saw the highest revenue (₹9.96 Cr), but this momentum was lost in 2025.
- **Breaking the Ceiling:** To move beyond ₹9.9 Cr/year, Swiggy must look at horizontal expansion (new cities) or vertical expansion (Instamart/Genie) as the current market appears saturated.

---

### 4.2 Monthly & Quarterly Revenue

**Goal:** Identify seasonal spikes, low-revenue periods, and the best-performing quarter.

```python
# Monthly Revenue Trend
monthly_revenue = delivered_orders.groupby(
    [delivered_orders['order_date'].dt.to_period('M')]
)['total_amount'].sum().reset_index()

# Quarterly Revenue Analysis
quarterly_revenue = delivered_orders.groupby(['order_year', 'order_quarter']).agg({
    'order_id':     'count',
    'total_amount': 'sum'
}).round(2)
```

**📊 Chart:**

![Monthly Revenue Trend](../Visuals/monthly_revenue_trend.png)

>*Line chart showing monthly revenue from January 2022 to December 2025, with markers at each data point.*

### 💡 Key Insights

- **Holiday Surge:** December, January, and July consistently peak at ₹8.5M+, correlating with holiday seasons and mid-year breaks.
- **The February Slump:** Revenue drops 10–12% every February — a systemic trend requiring an "Off-Season" marketing strategy.
- **The July Spike:** July consistently outperforms surrounding months, likely due to monsoon seasons driving higher home-delivery demand.

---

### 4.3 Revenue Drivers — City, Cuisine, Time

#### Revenue by City

```python
city_revenue = delivered_orders.groupby('city').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean'],
    'user_id':      'nunique'
}).round(2)

city_revenue.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value', 'Customers']
city_revenue['Revenue_per_Customer'] = (city_revenue['Total_Revenue'] / city_revenue['Customers']).round(2)
city_revenue = city_revenue.sort_values('Total_Revenue', ascending=False)
```

**Output — Revenue by City:**

| City | Total Revenue | Revenue per Customer | AOV |
|---|---|---|---|
| Mumbai | ₹8.76 Cr (22%) | ₹9,386 | ~₹697 |
| Delhi | High | High | ~₹695 |
| Bangalore | High | High | ~₹695 |
| Pune | Mid | Mid | ₹712 (highest AOV) |
| Jaipur | Lower | High per restaurant | ₹708 |
| Ahmedabad | ~3% | Low | ~₹695 |
| Lucknow | ~3% | Low | ~₹695 |

**📊 Chart:**

![Revenue by City](../Visuals/revenue_by_city.png)

>*Horizontal bar chart of total revenue by city (2022–2025).*

#### Revenue by Cuisine

```python
cuisine_revenue = delivered_orders.groupby('cuisine').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

cuisine_revenue.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value']
cuisine_revenue = cuisine_revenue.sort_values('Total_Revenue', ascending=False)
```

**Output — Top Cuisines:**

| Cuisine | Revenue | AOV |
|---|---|---|
| Seafood | ₹2.36 Cr | High |
| Beverages | ₹2.36 Cr | High |
| Chinese | 7th in volume | ₹716 (highest AOV) |
| North Indian | 10th | Lower |

**📊 Chart:**

![Top 10 Cuisines by Revenue](../Visuals/top_10_cuisines_revenue.png)

>*Horizontal bar chart showing top 10 cuisines ranked by total revenue.*

#### Revenue by Day Type & Time Slot

```python
# Revenue by Day Type
day_type_revenue = delivered_orders.groupby('day_type').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

# Revenue by Time Slot
time_slot_revenue = delivered_orders.groupby('time_slot').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

# Reorder by meal time
time_order = ['Breakfast', 'Lunch', 'Snack', 'Dinner', 'Late Night']
time_slot_revenue = time_slot_revenue.reindex(time_order)
```

**Output:**

| Day Type | Revenue Share |
|---|---|
| Weekday | 71.4% |
| Weekend | 28.6% |

| Time Slot | Revenue Share |
|---|---|
| Lunch | ~43% |
| Dinner | ~44% |
| Snack | ~4.6% |
| Late Night | ~2% |
| Breakfast | ~6% |

**📊 Chart:**

![Revenue Day Type and Time Slot](../Visuals/revenue_day_type_time_slot.png)

>*Left: Bar chart of revenue by day type (Weekday vs Weekend). Right: Bar chart of revenue by time slot.*

### 💡 Key Insights

- **"Big Three" Dominance:** Mumbai, Delhi, and Bangalore contribute ₹21.8 Cr (55%) of total revenue.
- **The Pune Premium:** Pune has the highest AOV (₹712) — focus should be on increasing order frequency there.
- **The Double-Peak Model:** Lunch and Dinner together drive 87.4% of revenue; the platform sits nearly idle during Snack and Late Night hours.
- **Strategic "Drink-Up" Bundling:** Since Beverages is a top revenue driver, implement "Cuisine + Beverage" cross-selling at checkout.

---

### 4.4 Average Order Value (AOV) Analysis

**Goal:** Understand how AOV varies across customer segments, age groups, and restaurant types to identify upselling opportunities.

```python
# AOV by Customer Segment
aov_by_segment = orders_with_rfm.groupby('segment')['total_amount'].mean().sort_values(ascending=False).round(2)

# AOV by Age Group
aov_by_age = delivered_orders.groupby('age_group')['total_amount'].mean().sort_values(ascending=False).round(2)

# AOV by Restaurant Type
aov_by_type = delivered_orders.groupby('restaurant_type')['total_amount'].mean().round(2)
```

**Output:**

| Dimension | Highest AOV | Lowest AOV |
|---|---|---|
| Customer Segment | Loyal Customers (₹727) | Hibernating (₹634) |
| Age Group | Near-identical across all groups | Gap < 0.5% |
| Restaurant Type | Traditional (₹698) | Cloud Kitchen (₹685) |

**📊 Charts:**

![AOV by Customer Segment](../Visuals/aov_by_customer_segment.png)

>*Horizontal bar chart of Average Order Value (AOV) across all RFM customer segments.*

![AOV by Age and Restaurant Type](../Visuals/aov_age_restaurant_type.png)

>*Left: Bar chart of AOV by age group. Right: Bar chart comparing AOV for Cloud Kitchen vs Traditional restaurants.*

### 💡 Key Insights

- **The "Engagement-to-Spend" Gap:** 14.6% spread between Loyalists (₹727) and Hibernating users (₹634) — engagement directly drives basket size.
- **Demographic Uniformity:** Only a 0.5% difference in AOV across all age groups — the platform has universal pricing appeal.
- **Traditional Trust Premium:** Traditional restaurants command a 2% higher AOV — customers still pay a slight premium for established physical brands.

---

### 4.5 Seasonal Patterns

**Goal:** Aggregate monthly revenue across all years to identify seasonality patterns for proactive marketing.

```python
monthly_pattern = delivered_orders.groupby('order_month').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

monthly_pattern.columns = ['Orders', 'Revenue', 'Avg_Order_Value']
monthly_pattern.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

best_month  = monthly_pattern['Revenue'].idxmax()
worst_month = monthly_pattern['Revenue'].idxmin()
```

**📊 Charts:**

![Monthly Revenue Pattern Bar](../Visuals/monthly_revenue_pattern.png)

>*Bar chart showing total aggregated monthly revenue across all four years (2022–2025).*

![Monthly AOV Trend Line](../Visuals/monthly_aov_trend.png)

>*Line chart showing monthly Average Order Value (AOV) trend with value annotations on each data point.*

### 💡 Key Insights

- **Best Month:** July / December consistently peak.
- **Worst Month:** February — a consistent ~10-12% revenue dip every year.
- **Recommendation:** Launch an "Off-Season" campaign for February (e.g., Valentine's Day Combos, Winter Warmers) to recover the revenue gap.

---

## 5️⃣. 🏪Restaurant Partner Performance Analysis

> **Business Challenge #3 — Questions Answered:**
> - Which restaurants generate the most revenue?
> - How does rating impact order volume?
> - Cloud Kitchen vs Traditional performance?
> - Which cuisines are most popular per city?
> - Which restaurants need support or removal?

---

### 5.1 Top & Bottom Restaurant Revenue

**Goal:** Rank all restaurants by total revenue to identify star performers and underperformers.

```python
restaurant_performance = delivered_orders.groupby(
    ['restaurant_id', 'restaurant_name', 'city', 'cuisine']
).agg({
    'order_id':          'count',
    'total_amount':      ['sum', 'mean'],
    'restaurant_rating': 'first'
}).round(2)

restaurant_performance.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value', 'Rating']
restaurant_performance = restaurant_performance.sort_values('Total_Revenue', ascending=False)
```

**Output — Top 10 Restaurants:**
- All maintain a Rating of 4.5+
- AOV consistently above ₹1,000
- #1 Restaurant: **Spicy Hub (Mumbai)** — beverage-focused, AOV ₹1,090

**📊 Chart:**

![Top 15 Restaurants by Revenue](../Visuals/top_15_restaurants_revenue.png)

>*Horizontal bar chart of the top 15 restaurants ranked by total revenue (2022–2025), with labels in Lakhs.*

**Output — Bottom 10 Restaurants:**
- AOV stuck below ₹460
- Similar order volumes to top performers
- Very low repeat customer rate

**📊 Chart:**

![Bottom 10 Underperforming Restaurants](../Visuals/bottom_10_restaurants_revenue.png)

>*Horizontal bar chart of the bottom 10 restaurants by revenue, highlighted in red.*

### 💡 Key Insights

- **The AOV Multiplier:** Top restaurants generate ~₹6 Lakhs while bottom ones generate ~₹2.2 Lakhs. Since order counts are nearly identical, the gap is entirely driven by Menu Engineering and Ticket Size.
- **Elite Quality Bar:** All Top 10 restaurants maintain a Rating of 4.5+, proving that high customer satisfaction is a prerequisite for commanding premium AOV.
- **The "Spicy Hub" Anomaly:** The #1 restaurant primarily sells beverages — proving that beverage-focused outlets can be high-revenue drivers if positioned as premium brands.

---

### 5.2 Rating Impact Analysis

**Goal:** Determine whether restaurant rating drives order volume and if there is a "quality premium" in terms of AOV.

```python
rating_performance = delivered_orders.groupby('rating_bucket').agg({
    'order_id':        'count',
    'total_amount':    ['sum', 'mean'],
    'restaurant_id':   'nunique'
}).round(2)

rating_performance.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value', 'Restaurants']
rating_performance['Orders_per_Restaurant'] = (rating_performance['Orders'] / rating_performance['Restaurants']).round(2)

# Correlation between rating and order count
rating_orders_corr = delivered_orders.groupby('restaurant_id').agg({
    'restaurant_rating': 'first',
    'order_id':          'count'
})

correlation = rating_orders_corr.corr().iloc[0, 1]
```

**Output:**

| Rating Bucket | Restaurants | Orders/Restaurant | AOV |
|---|---|---|---|
| Excellent (4.5+) | — | ~570 | ₹778 |
| Very Good (4.0–4.5) | — | ~570 | ~₹700 |
| Good (3.5–4.0) | 489 (largest group) | ~570 | ₹638 |
| Average (<3.5) | 76 | ~568 | Lower |

**Correlation Result:** Rating vs Order Count = **-0.002** (near-zero correlation)

**📊 Chart:**

![Order Volume by Rating Bucket](../Visuals/order_volume_by_rating.png)

>*Bar chart showing total order volume for each restaurant rating bucket.*

### 💡 Key Insights

- **The Quality Paradox:** Near-zero correlation between ratings and order volume — marketing, cuisine, or proximity drives volume more than satisfaction.
- **The Revenue Efficiency Premium:** While order counts are flat, "Excellent" restaurants (4.5+) have a 22% higher AOV (₹778) than "Good" restaurants (₹638).
- **The Floor Effect:** Even "Average" restaurants maintain high volumes, indicating a high "Crave" factor on the platform.
- **Key Opportunity:** Moving the 489 "Good" bucket restaurants to "Very Good" would unlock an extra ₹117 per order.

---

### 5.3 Cloud Kitchen vs Traditional Performance

**Goal:** Compare operational efficiency between the two restaurant models.

```python
cloud_vs_traditional = delivered_orders.groupby('restaurant_type').agg({
    'restaurant_id': 'nunique',
    'order_id':      'count',
    'total_amount':  ['sum', 'mean'],
    'user_id':       'nunique'
}).round(2)

cloud_vs_traditional.columns = ['Restaurants', 'Orders', 'Total_Revenue', 'Avg_Order_Value', 'Customers']
cloud_vs_traditional['Orders_per_Restaurant']    = (cloud_vs_traditional['Orders'] / cloud_vs_traditional['Restaurants']).round(2)
cloud_vs_traditional['Revenue_per_Restaurant']   = (cloud_vs_traditional['Total_Revenue'] / cloud_vs_traditional['Restaurants']).round(2)
cloud_vs_traditional['Customers_per_Restaurant'] = (cloud_vs_traditional['Customers'] / cloud_vs_traditional['Restaurants']).round(2)
```

**Output:**

| Metric | Cloud Kitchen | Traditional |
|---|---|---|
| Orders per Restaurant | ~570 | ~570 |
| Revenue per Restaurant | Slightly lower | Slightly higher |
| AOV | ₹685 | ₹698 |
| Customers per Restaurant | **33.8** | **14.0** |

**📊 Chart:**

![Cloud Kitchen vs Traditional Efficiency](../Visuals/cloud_vs_traditional_efficiency.png)

>*Grouped bar chart comparing Orders per Restaurant and Revenue per Restaurant for Cloud Kitchen vs Traditional.*

### 💡 Key Insights

- **Volume Neutrality:** Both models carry ~570 orders/restaurant — operational load is the same regardless of model.
- **The "Brand Premium":** Traditional outlets command a 2% higher AOV — customers still associate physical locations with premium value.
- **The Acquisition Powerhouse:** Cloud Kitchens reach 2.4x more unique customers per partner (33.8 vs 14.0).
- **Strategic Specialization:** Use Traditional partners for high-AOV "Dinner/Occasion" categories; use Cloud Kitchens for high-reach "Lunch/Snack" customer acquisition.

---

### 5.4 Cuisine Performance by City

**Goal:** Find which cuisines dominate each city and identify expansion opportunities.

```python
cuisine_city_performance = delivered_orders.groupby(['city', 'cuisine']).agg({
    'order_id':       'count',
    'total_amount':   'sum',
    'restaurant_id':  'nunique'
}).round(2)

cuisine_city_performance.columns = ['Orders', 'Revenue', 'Restaurants']
cuisine_city_performance = cuisine_city_performance.sort_values(['city', 'Revenue'], ascending=[True, False])

# Top 3 cuisines per city
top_cuisines_per_city = cuisine_city_performance.groupby('city').head(3)
```

**Output — Notable City-Cuisine Patterns:**

| City | #1 Cuisine | Insight |
|---|---|---|
| Mumbai | Italian | Tier-1 prefers international/premium |
| Delhi | Healthy Food | Blueprint for health-first market |
| Chennai | Continental | Despite coastal location — high Veg demand |
| Jaipur | Thai | #1 revenue driver with only 5 restaurants — massive gap |
| Ahmedabad | Mughlai | Surprising for a traditionally vegetarian city |

**📊 Chart:**

![Top 10 Cuisines by Revenue — Restaurant Section](../Visuals/top_10_cuisines_restaurant_section.png)

>*Horizontal bar chart showing top 10 cuisines by total revenue (from restaurant analysis perspective).*

### 💡 Key Insights

- **The Jaipur Thai Opportunity:** Thai is Jaipur's #1 revenue driver with only 5 restaurants — this niche is massively underserved and should be aggressively expanded.
- **Healthy Delhi Blueprint:** 14 Delhi restaurants in Healthy Food generating ₹5.7M — replicate this model in Bangalore/Mumbai.
- **The Ahmedabad "Niche":** Mughlai dominates in Ahmedabad despite it being known for vegetarian culture — data challenges standard assumptions.

---

### 5.5 Restaurant Efficiency & Underperformers

**Goal:** Calculate detailed efficiency metrics per restaurant and identify the bottom 10% of performers.

```python
restaurant_efficiency = delivered_orders.groupby(
    ['restaurant_id', 'restaurant_name', 'city', 'restaurant_type']
).agg({
    'order_id':          'count',
    'total_amount':      'sum',
    'user_id':           'nunique',
    'restaurant_rating': 'first'
}).round(2)

restaurant_efficiency.columns = ['Total_Orders', 'Total_Revenue', 'Unique_Customers', 'Rating']
restaurant_efficiency['Revenue_per_Order']    = (restaurant_efficiency['Total_Revenue'] / restaurant_efficiency['Total_Orders']).round(2)
restaurant_efficiency['Orders_per_Customer']  = (restaurant_efficiency['Total_Orders'] / restaurant_efficiency['Unique_Customers']).round(2)

# Identify bottom 10% underperformers
underperforming_threshold      = restaurant_efficiency['Total_Revenue'].quantile(0.1)
underperforming_restaurants    = restaurant_efficiency[restaurant_efficiency['Total_Revenue'] < underperforming_threshold]

# Financial impact
avg_restaurant_revenue    = restaurant_efficiency['Total_Revenue'].mean()
underperformer_revenue    = underperforming_restaurants['Total_Revenue'].sum()
potential_loss            = (avg_restaurant_revenue * len(underperforming_restaurants)) - underperformer_revenue
```

**Output:**

| Metric | Value |
|---|---|
| Underperforming Restaurants | ~100 (bottom 10%) |
| Revenue Threshold | <₹2.5 Lakhs |
| Orders per Customer | ~1.09 (near-zero retention) |
| Potential Revenue Loss | **₹1.08 Crores** |

### 💡 Key Insights

- **The Efficiency Trap:** Underperformers process ~560 orders but generate 65% less revenue than top stars.
- **One-and-Done Business:** With 1.09 orders-per-customer, underperforming restaurants fail to convert discovery into loyalty.
- **"AOV or Out":** Underperformers should be given a 90-day window to increase AOV by 25% through menu bundling or face reduced visibility.
- **Financial Impact:** Replacing the bottom 100 with partners at platform average (₹3.96L) could unlock ₹1.1 Crores in annual revenue.

---

## 6️⃣. 🍽️Menu & Product Optimization

> **Business Challenge #4 — Questions Answered:**
> - What are the best-selling menu items?
> - Veg vs Non-Veg preferences?
> - Optimal price range for different categories?
> - Which items are frequently ordered together?
> - Which items drive the highest revenue?

---

### 6.1 Best-Selling Items Analysis

**Goal:** Rank menu items by volume and revenue to find platform bestsellers.

```python
top_items = order_items_master.groupby(['item_name', 'category', 'item_type']).agg({
    'order_item_id': 'count',
    'line_total':    'sum',
    'menu_price':    'mean'
}).round(2)

top_items.columns = ['Times_Ordered', 'Total_Revenue', 'Avg_Price']
top_items = top_items.sort_values('Times_Ordered', ascending=False)

# Top items per category
top_items_by_category = order_items_master.groupby(['category', 'item_name']).agg({
    'order_item_id': 'count',
    'line_total':    'sum'
}).reset_index()

top_by_cat = top_items_by_category.groupby('Category').head(5)
```

**Output — Notable Top Items:**

| Item | Category | Times Ordered | Revenue |
|---|---|---|---|
| Paneer Burger | Burger | Top seller | ₹1.45 Cr |
| Cheese Burger | Burger | Very high | High |
| Coffee | Beverages | 31,000+ | Lower unit price |
| Brownie | Desserts | High volume | Lower revenue |

**📊 Chart:**

![Top 15 Best-Selling Items](../Visuals/top_15_bestselling_items.png)

>*Horizontal bar chart of the top 15 best-selling menu items ranked by number of orders.*

### 💡 Key Insights

- **The Burger & Pizza Duopoly:** These two categories own the top 11 spots for revenue — the platform's primary identity is Fast Food Delivery.
- **Paneer Dominance:** Paneer Burger alone generated ₹1.45 Cr — overwhelming preference for vegetarian premium fast food.
- **The Perfect Pair Strategy:** Since Roti and Coffee are high-volume but low-price, create mandatory bundles (e.g., "Meal + Drink") to increase basket value.
- **Dessert Potential:** 7 different desserts in the top 20 — introduce Dessert Platters or Family Packs (₹400+) to convert high volume into higher revenue.

---

### 6.2 Veg vs Non-Veg Analysis

**Goal:** Understand dietary preferences across the platform, by city, and by age group.

```python
# Overall preference
veg_vs_nonveg = order_items_master.groupby('item_type').agg({
    'order_item_id': 'count',
    'line_total':    'sum',
    'menu_price':    'mean'
}).round(2)

veg_vs_nonveg['%_of_Orders']  = (veg_vs_nonveg['Items_Ordered'] / veg_vs_nonveg['Items_Ordered'].sum() * 100).round(1)
veg_vs_nonveg['%_of_Revenue'] = (veg_vs_nonveg['Total_Revenue'] / veg_vs_nonveg['Total_Revenue'].sum() * 100).round(1)

# By City
veg_by_city = order_items_master.merge(orders_master[['order_id', 'city']], on='order_id')
veg_by_city = veg_by_city.groupby(['city', 'item_type'])['order_item_id'].count().unstack(fill_value=0)
veg_by_city['Veg_%']     = (veg_by_city['Veg'] / (veg_by_city['Veg'] + veg_by_city['Non-Veg']) * 100).round(1)
```

**Output:**

| Item Type | % of Orders | % of Revenue | Avg Price |
|---|---|---|---|
| Veg | **82.2%** | **76.2%** | ₹171.71 |
| Non-Veg | 17.8% | 23.8% | ₹247.51 |

**By City — Veg % Highlights:**

| City | Veg % |
|---|---|
| Chennai | 83.5% |
| Jaipur | 83%+ |
| Ahmedabad | 83%+ |
| Lucknow | ~81% |
| Pune | ~81% |

**📊 Chart:**

![Veg vs Non-Veg Revenue](../Visuals/veg_nonveg_revenue.png)

>*Bar chart comparing total revenue from Veg vs Non-Veg items.*

### 💡 Key Insights

- **Veg Dominance:** Swiggy is primarily a "Green" platform with 82.2% Veg order volume.
- **The Premium Gap:** Non-Veg items average ₹247.51 vs Veg ₹171.71 — moving a customer from Veg Burger to Non-Veg Burger adds ₹75 in revenue per order.
- **Universal Palate:** Diet preference is cultural/geographic, not generational — all age groups show nearly identical ~82% Veg split.
- **Chennai Surprise:** Despite being a coastal city, Chennai shows 83.5% Veg preference for daily orders, but splurges on Seafood for occasions.

---

### 6.3 Price Category Analysis

**Goal:** Understand which price tiers drive the most orders and identify pricing strategy opportunities.

```python
price_category_performance = order_items_master.groupby('price_category').agg({
    'order_item_id': 'count',
    'line_total':    'sum',
    'menu_price':    'mean'
}).round(2)

price_category_performance['%_of_Orders'] = (price_category_performance['Items_Ordered'] / price_category_performance['Items_Ordered'].sum() * 100).round(1)

# Price analysis by category
optimal_price = order_items_master.groupby('category').agg({
    'menu_price':    ['min', 'mean', 'median', 'max', 'std'],
    'order_item_id': 'count'
}).round(2)
```

**Output — Price Category Distribution:**

| Price Category | % of Orders | Revenue Contribution |
|---|---|---|
| Budget (<₹100) | 21% | 8% of revenue |
| Economic (₹100–₹199) | **45%** | Backbone |
| Mid-Range (₹200–₹299) | 17% | High potential |
| Premium (₹300–₹399) | ~12% | Good margin |
| Luxury (₹400+) | 4.7% | ₹4.76 Cr (disproportionate) |

**📊 Chart:**

![Orders by Price Category](../Visuals/orders_by_price_category.png)

>*Bar chart showing number of items ordered in each price category.*

### 💡 Key Insights

- **The "Economic" Backbone:** ₹100–₹199 is the volume driver (45% of all orders) — daily habitual users live here.
- **The Luxury Gap:** Only 4.7% of orders are Luxury (₹400+), yet they contribute a disproportionately high ₹4.76 Cr.
- **The "Mass-Premium" Opportunity:** Moving customers from "Economic" to "Mid-Range" (₹200–₹299) is the most realistic path to breaking revenue stagnation.

---

### 6.4 Basket Analysis (Items Ordered Together)

**Goal:** Discover which item pairs are frequently ordered together to design effective combo deals.

```python
orders_with_items = order_items_master.groupby('order_id')['item_name'].apply(list).reset_index()
orders_with_items['item_count'] = orders_with_items['item_name'].apply(len)

multi_item_orders = orders_with_items[orders_with_items['item_count'] >= 2]

# Most common 2-item combinations
from itertools import combinations

combo_list = []
for items in multi_item_orders['item_name']:
    if len(items) >= 2:
        for combo in combinations(sorted(items), 2):
            combo_list.append(combo)

combo_df     = pd.DataFrame(combo_list, columns=['Item1', 'Item2'])
combo_counts = combo_df.groupby(['Item1', 'Item2']).size().sort_values(ascending=False).head(20)
```

**Output:**

| Metric | Value |
|---|---|
| Orders with 2+ items | 85% of all orders |
| Single item orders | 15% |
| Average items per order | **2.78 items** |

**Top Combinations:** Cheese Burger + Paneer Burger, and similar Burger + Burger pairs dominate the top 3.

### 💡 Key Insights

- **The Group-Order Engine:** 85% of orders are multi-item with avg 2.78 items — these are "duo" orders (couples/friends), not solo meals.
- **The Burger-Burger Paradox:** People aren't buying a meal — they are buying for two people.
- **The Missing Side-Kick:** Beverages and Desserts only appear in the bottom half of the top 20 pairs — a clear cross-sell opportunity.
- **The Dessert "Hook":** Gulab Jamun and Rasmalai are the only non-savory items in Top 20. Nudging this pairing at checkout via "Frequently Bought Together" could scale to 50k+ orders.

---

### 6.5 Revenue & Margin Analysis by Category

**Goal:** Understand which menu categories contribute the most to platform revenue.

```python
category_performance = order_items_master.groupby('category').agg({
    'order_item_id': 'count',
    'line_total':    'sum',
    'menu_price':    'mean'
}).round(2)

category_performance['%_of_Revenue'] = (category_performance['Total_Revenue'] / category_performance['Total_Revenue'].sum() * 100).round(1)
category_performance = category_performance.sort_values('Total_Revenue', ascending=False)
```

**Output — Category Revenue:**

| Category | Revenue Share |
|---|---|
| Main Course | **26.6%** (₹11.1 Cr) |
| Pizza | ~17% |
| Burger | ~18% |
| Desserts + Beverages | ~17% combined |

**📊 Chart:**

![Revenue by Menu Category](../Visuals/revenue_by_menu_category.png)

>*Bar chart of total revenue broken down by menu category.*

### 💡 Key Insights

- **Main Course Supremacy:** Main Courses are the platform's financial anchor at ₹11.1 Cr (26.6%) with Revenue per Order of ₹450+.
- **The Pizza/Burger "Volume Engine":** Together they drive 35% of revenue — lower price points but high frequency.
- **Pure Margin Potential:** Desserts and Beverages represent 17% of revenue with near-zero extra delivery cost when bundled with existing orders.

---

## 7️⃣. ⚡Operational Efficiency Analysis

> **Business Challenge #5 — Questions Answered:**
> - What is the hourly/daily order distribution pattern?
> - When are peak ordering times?
> - What is the cancellation rate by city/time/restaurant?
> - Why are orders being cancelled?
> - What is the weekend vs weekday demand difference?

---

### 7.1 Order Distribution Patterns

**Goal:** Map out when orders are placed across time slots and days of the week.

```python
# Order distribution by time slot
time_slot_distribution = delivered_orders.groupby('time_slot').agg({
    'order_id':     'count',
    'total_amount': 'sum'
}).round(2)

time_slot_distribution['%_of_Orders'] = (time_slot_distribution['Orders'] / time_slot_distribution['Orders'].sum() * 100).round(1)
time_slot_distribution = time_slot_distribution.reindex(['Breakfast', 'Lunch', 'Snack', 'Dinner', 'Late Night'])

# Daily distribution (day of week)
daily_distribution = delivered_orders.groupby(['day_of_week']).agg({
    'order_id':     'count',
    'total_amount': 'sum'
}).reset_index()

daily_distribution['day_name'] = daily_distribution['day_of_week'].map({
    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
    4: 'Friday', 5: 'Saturday', 6: 'Sunday'
})
```

**Output — Time Slot Distribution:**

| Time Slot | % of Orders |
|---|---|
| Lunch | ~43% |
| Dinner | ~44% |
| Breakfast | ~6% |
| Snack | ~4% |
| Late Night | ~3% |

**Output — Busiest Day:** **Monday**

**📊 Charts:**

![Orders by Time Slot](../Visuals/orders_by_time_slot.png)

>*Bar chart of total delivered orders distributed across five time slots.*

![Weekly Order Distribution](../Visuals/weekly_order_distribution.png)

>*Bar chart showing total orders for each day of the week (Monday–Sunday).*

### 💡 Key Insights

- **The Lunch/Dinner Monolith:** 87.5% of all orders in just two windows — the system handles 28x more volume at Lunch than at Late Night.
- **The "Snack" Slump:** Snacks and Late Night together account for only 6.3% — delivery infrastructure is vastly underutilized for 70% of the operating day.
- **The Monday "Office" Surge:** Monday is the busiest day — confirming the platform is heavily driven by Corporate/Office Lunch orders.

---

### 7.2 Peak Hours & Capacity Analysis

**Goal:** Calculate the capacity requirements to handle peak demand and quantify the demand spike ratio.

```python
# Peak analysis by time slot and day type
peak_analysis = delivered_orders.groupby(['time_slot', 'day_type']).agg({
    'order_id':     'count',
    'total_amount': 'sum'
}).round(2)

# Capacity calculations
operating_hours       = 14  # 8 AM – 10 PM
total_days            = (delivered_orders['order_date'].max() - delivered_orders['order_date'].min()).days
avg_orders_per_hour   = len(delivered_orders) / (total_days * operating_hours)
peak_time_orders      = time_slot_distribution['Orders'].max()
peak_slot_hours       = 3
peak_capacity_per_hour = peak_time_orders / (total_days * peak_slot_hours / 365)
```

**Output:**

| Metric | Value |
|---|---|
| Average orders per hour | ~28 |
| Peak capacity needed | ~21,245 orders/hour |
| Capacity Multiplier | **761x average** |
| Weekday Lunch Revenue | ₹126M |
| Weekend Lunch Revenue | ₹50M |

### 💡 Key Insights

- **The 761x Surge:** Infrastructure must jump from 28 orders/hour to 21,245/hour — a massive tech and human resource strain.
- **The Weekday War:** Weekday Lunch generates 60% more than Weekend Lunch — 60% more riders needed on Tuesday than Saturday.
- **"Micro-Shift" Strategy:** Move from "Full-Day" partner contracts to "Micro-Shifts" focused on the 4-hour high-volume windows (11 AM–2 PM and 7–9 PM).

---

### 7.3 Cancellation Analysis

**Goal:** Calculate the total cancellation rate, identify high-cancellation cities/restaurants/times, and quantify revenue loss.

```python
# Overall cancellation metrics
total_orders_all      = len(orders_master)
cancelled_orders      = (orders_master['order_status'] == 'Cancelled').sum()
cancellation_rate     = (cancelled_orders / total_orders_all) * 100
cancelled_revenue     = orders_master[orders_master['order_status'] == 'Cancelled']['total_amount'].sum()

# Cancellation by city
cancellation_by_city = orders_master.groupby('city').agg({
    'order_id':     'count',
    'order_status': lambda x: (x == 'Cancelled').sum()
}).reset_index()

cancellation_by_city['Cancellation_Rate_(%)'] = (cancellation_by_city['Cancelled'] / cancellation_by_city['Total_Orders'] * 100).round(2)
cancellation_by_city = cancellation_by_city.sort_values('Cancellation_Rate_(%)', ascending=False)

# Cancellation by restaurant (min 50 orders)
cancellation_by_restaurant = orders_master.groupby(['restaurant_id', 'restaurant_name']).agg({
    'order_id':     'count',
    'order_status': lambda x: (x == 'Cancelled').sum()
}).reset_index()

cancellation_by_restaurant['cancellation_rate'] = (cancellation_by_restaurant['cancelled'] / cancellation_by_restaurant['total_orders'] * 100).round(2)
significant_restaurants = cancellation_by_restaurant[cancellation_by_restaurant['total_orders'] >= 50]
significant_restaurants = significant_restaurants.sort_values('cancellation_rate', ascending=False)

# Cancellation by time slot
cancellation_by_time = orders_master.groupby('time_slot').agg({
    'order_id':     'count',
    'order_status': lambda x: (x == 'Cancelled').sum()
}).reset_index()
```

**Output:**

| Metric | Value |
|---|---|
| Overall Cancellation Rate | **4.95%** |
| Total Cancelled Orders | 29,719 |
| Monthly Lost Revenue | ₹2.08 Crores |
| Annual Lost Revenue | **₹25 Crores** |

**By City (Highest Cancellation):**

| City | Cancellation Rate |
|---|---|
| Delhi | 5.09% |
| Kolkata | 5.09% |
| Others | ~4.9% |

**By Time Slot (Highest):** Late Night — 5.18%

**By Restaurant — Red Flag:** Restaurant R0139 "The Spice" — **7.57%** (50% above platform average)

**📊 Chart:**

![Cancellation Rate by City](../Visuals/cancellation_rate_by_city.png)

>*Horizontal bar chart of cancellation rates per city, sorted from highest to lowest.*

### 💡 Key Insights

- **₹25 Crore Annual Drain:** Monthly lost revenue of ₹2.08 Cr projects to ₹25 Cr annually — direct EBITDA impact.
- **The Delhi Pressure:** Higher cancellations in Delhi/Kolkata likely correlate with traffic congestion and extreme weather.
- **The "Ghost" Slot:** Late Night has the highest cancellation (5.18%) — restaurants close without updating their status.
- **The "7% Ceiling":** 20 restaurants consistently at 7%+ cancellation rate. Bringing them to the platform average (4.95%) could save ₹1.8 Lakhs/month.

---

### 7.4 Weekend vs Weekday Demand

**Goal:** Quantify the demand difference between weekdays and weekends to inform fleet and marketing decisions.

```python
weekend_weekday_ops = delivered_orders.groupby('day_type').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean'],
    'user_id':      'nunique'
}).round(2)

weekend_weekday_ops.columns = ['Orders', 'Total_Revenue', 'Avg_Order_Value', 'Unique_Customers']
weekend_weekday_ops['Days']                = weekend_weekday_ops.index.map({'Weekday': 5, 'Weekend': 2})
weekend_weekday_ops['Avg_Orders_per_Day']  = (weekend_weekday_ops['Orders'] / weekend_weekday_ops['Days']).round(0)
weekend_weekday_ops['Avg_Revenue_per_Day'] = (weekend_weekday_ops['Total_Revenue'] / weekend_weekday_ops['Days']).round(2)
weekend_weekday_ops['Demand_Index']        = (weekend_weekday_ops['Avg_Orders_per_Day'] / weekday_avg * 100).round(0)
```

**Output:**

| Day Type | Avg Orders/Day | Revenue Share | Unique Customers |
|---|---|---|---|
| Weekday | ~81,000 | 71.4% | ~10,000 |
| Weekend | ~81,000 | 28.6% | ~9,686 |

**📊 Chart:**

![Avg Orders per Day Weekend vs Weekday](../Visuals/weekend_weekday_orders.png)

>*Bar chart comparing average orders per day between Weekday and Weekend.*

### 💡 Key Insights

- **The Utility Plateau:** Near-zero difference (0.2%) in order volume between weekdays and weekends — Swiggy is a 7-day utility, not a weekend treat.
- **Uniform Fleet Requirement:** No surge fleet needed for weekends — a consistent, full-time 7-day fleet is required.
- **The "Routine" Customer:** Nearly identical unique customers on weekdays (~10,000) and weekends (~9,686) — same group using the app every day, signaling strong habit formation.
- **Missing Weekend Opportunity:** Lack of weekend spike suggests Swiggy isn't capturing the "Group/Family Dining" market that typically peaks on Saturdays.

---

## 8️⃣. 🌏Market Expansion & Growth Analysis

> **Business Challenge #6 — Questions Answered:**
> - Which cities show highest revenue per restaurant?
> - Which cities have room for more restaurants?
> - What is optimal restaurant density per city?
> - Which cuisines are underrepresented where?
> - Where should we expand next?

---

### 8.1 City Performance Metrics

**Goal:** Build a comprehensive metric table for each city to assess current performance and efficiency.

```python
city_expansion_metrics = delivered_orders.groupby('city').agg({
    'restaurant_id': 'nunique',
    'order_id':      'count',
    'total_amount':  'sum',
    'user_id':       'nunique'
}).round(2)

city_expansion_metrics.columns = ['Restaurants', 'Orders', 'Revenue', 'Customers']
city_expansion_metrics['Orders_per_Restaurant']    = (city_expansion_metrics['Orders'] / city_expansion_metrics['Restaurants']).round(2)
city_expansion_metrics['Revenue_per_Restaurant']   = (city_expansion_metrics['Revenue'] / city_expansion_metrics['Restaurants']).round(2)
city_expansion_metrics['Customers_per_Restaurant'] = (city_expansion_metrics['Customers'] / city_expansion_metrics['Restaurants']).round(2)
city_expansion_metrics['Avg_Order_Value']          = (city_expansion_metrics['Revenue'] / city_expansion_metrics['Orders']).round(2)

city_expansion_metrics = city_expansion_metrics.sort_values('Revenue_per_Restaurant', ascending=False)
```

**Output — Key City Metrics:**

| City | Revenue/Restaurant | Customers/Restaurant | AOV |
|---|---|---|---|
| Jaipur | ~₹4L (highest) | 141 | ₹708 |
| Pune | ~₹4L | High | ₹711 |
| Hyderabad | ~₹4L | Mid | Mid |
| Mumbai | ~₹3.96L | **42** (lowest — over-supplied) | ~₹697 |
| Lucknow | Lower | **161** (highest — underserved) | ~₹695 |
| Ahmedabad | Lower | **155+** (underserved) | ~₹695 |

**📊 Chart:**

![Revenue per Restaurant by City](../Visuals/revenue_per_restaurant_city.png)

>*Horizontal bar chart of Revenue per Restaurant for each city — indicates profitability potential.*

### 💡 Key Insights

- **The Tier-2 Profit Paradox:** Jaipur, Pune, and Hyderabad lead in Revenue per Restaurant (~₹4L), more profitable than Mumbai or Delhi.
- **The Mumbai/Delhi Dilution:** Mumbai has 221 restaurants but only 42 customers/partner vs. Lucknow's 161. Mumbai is in "partner over-supply" phase.
- **The Lucknow & Ahmedabad Goldmine:** Highest customer-per-restaurant ratios (>155) — desperately underserved and highest ROI for new onboarding.

---

### 8.2 Market Saturation Analysis

**Goal:** Calculate how "crowded" each city's restaurant market is and generate an Expansion Priority Score.

```python
# Saturation Index
city_expansion_metrics['Saturation_Index'] = (
    city_expansion_metrics['Orders_per_Restaurant'] /
    city_expansion_metrics['Orders_per_Restaurant'].max() * 100
).round(0)

# Expansion Priority Score (40% Revenue Score + 30% Growth Score + 30% Revenue per Restaurant)
city_expansion_metrics['Revenue_Score'] = (
    city_expansion_metrics['Revenue_per_Restaurant'] /
    city_expansion_metrics['Revenue_per_Restaurant'].max() * 50
).round(0)

city_expansion_metrics['Growth_Score']        = (100 - city_expansion_metrics['Saturation_Index']) * 0.5
city_expansion_metrics['Expansion_Priority']  = (city_expansion_metrics['Revenue_Score'] + city_expansion_metrics['Growth_Score']).round(0)
```

**Output:**

| City | Saturation Index | Expansion Priority |
|---|---|---|
| Mumbai | 100% | Lower |
| Delhi | 100% | Lower |
| Bangalore | 100% | Higher (revenue saves it) |
| Jaipur | Near 100% | **50.00 (highest)** |

**📊 Chart:**

![Market Saturation Index](../Visuals/market_saturation_index.png)

>*Horizontal bar chart of Saturation Index per city. Higher = more crowded market.*

### 💡 Key Insights

- **The 100% Ceiling:** Major metros have reached 100% Saturation — adding a new restaurant doesn't create new demand; it just steals from existing ones.
- **The "Land Grab" Phase is Over:** All cities near 100% saturation confirms that Yield Optimization (extracting more revenue from existing restaurants via advertising and platform fees) is the next phase.
- **The "Jaipur Model":** Highest Expansion Priority (50.00) — gold standard: high revenue/restaurant + high customer density.

---

### 8.3 Cuisine Gap Analysis

**Goal:** Find cuisines that are underrepresented in specific cities compared to the platform average — these are expansion targets.

```python
cuisine_distribution = delivered_orders.groupby(['city', 'cuisine']).agg({
    'restaurant_id': 'nunique',
    'order_id':      'count'
}).reset_index()

cuisine_distribution.columns = ['City', 'Cuisine', 'Restaurants', 'Orders']

# Average restaurants per cuisine across all cities
avg_restaurants_per_cuisine = cuisine_distribution.groupby('Cuisine')['Restaurants'].mean()

# Identify gaps
cuisine_gaps = []
for city in cuisine_distribution['City'].unique():
    city_cuisines = cuisine_distribution[cuisine_distribution['City'] == city]
    for cuisine in avg_restaurants_per_cuisine.index:
        city_count = city_cuisines[city_cuisines['Cuisine'] == cuisine]['Restaurants'].values
        city_count = city_count[0] if len(city_count) > 0 else 0
        avg_count  = avg_restaurants_per_cuisine[cuisine]
        if city_count < avg_count:
            cuisine_gaps.append({'City': city, 'Cuisine': cuisine,
                                  'Current': city_count, 'Average': round(avg_count, 2),
                                  'Gap': round(avg_count - city_count, 2)})

cuisine_gap_df = pd.DataFrame(cuisine_gaps).sort_values('Gap', ascending=False)
```

**Output — Top Cuisine Gaps:**

| City | Underrepresented Cuisine | Gap Score |
|---|---|---|
| Ahmedabad | Beverages/Desserts | 6.56 |
| Ahmedabad | Healthy Food | 5.33 |
| Lucknow | Biryani | 6.12 |
| Lucknow | Thai | High |
| Jaipur | Beverages/Desserts | High |

### 💡 Key Insights

- **The "Biryani Paradox":** Lucknow, a Biryani capital, has a significant digital gap (6.12) — lack of consistent, quick-delivery Biryani brands.
- **The Ahmedabad "Health" Goldmine:** Ahmedabad has a gap of 5.33 in Healthy Food — highest ROI entry point for Cloud Kitchens as healthy food orders are growing 2x faster in Tier-2.
- **The Snack-Time Vacuum:** Beverages and Desserts gaps explain WHY the Snack slot (4–6 PM) underperforms — if these categories don't exist locally, demand can't be captured.

---

### 8.4 Market Penetration Analysis

**Goal:** Calculate what percentage of each city's total population is currently using Swiggy — to find the true growth headroom.

```python
city_tam = {
    'Mumbai': 20000000, 'Delhi': 18000000, 'Bangalore': 12000000,
    'Hyderabad': 10000000, 'Chennai': 10000000, 'Kolkata': 14000000,
    'Pune': 6000000, 'Ahmedabad': 8000000, 'Jaipur': 3500000, 'Lucknow': 3500000
}

penetration_analysis = city_expansion_metrics.copy()
penetration_analysis['Total_Population']       = penetration_analysis.index.map(city_tam)
penetration_analysis['Penetration_Rate_(%)']   = (penetration_analysis['Customers'] / penetration_analysis['Total_Population'] * 100).round(4)
penetration_analysis['Growth_Potential_(%)']   = (100 - penetration_analysis['Penetration_Rate_(%)']).round(2)

penetration_analysis = penetration_analysis.sort_values('Growth_Potential_(%)', ascending=False)
```

**Output:**

| City | Penetration Rate | Growth Potential |
|---|---|---|
| Jaipur | 0.13% (highest) | 99.87% |
| Lucknow | 0.12% | 99.88% |
| Pune | 0.11% | 99.89% |
| Mumbai | 0.05% | **99.95%** |
| Delhi | ~0.05% | ~99.95% |

**📊 Chart:**

![Market Penetration Rate by City](../Visuals/market_penetration_rate.png)

>*Bar chart showing current market penetration rate (%) for each city.*

### 💡 Key Insights

- **The 0.1% Threshold:** Swiggy is serving only the "Upper Crust" — less than 0.1% of population in most metros.
- **The "Mass Market" Gap:** 99.9% of the population is yet to order — growth is about "Deepening" into Tier-1 suburbs and lower-income demographics.
- **The 45 Million Opportunity:** Across these 10 cities, ~45 million middle-income smartphone users haven't yet ordered on Swiggy.
- **The "Swiggy Lite" Concept:** Mumbai's 0.05% penetration suggests high fees are a barrier for the middle 40% — a lower-cost, slightly slower service could unlock massive new demand.

---

### 8.5 Final Expansion Recommendation

**Goal:** Combine all expansion metrics into a single weighted Final Score to produce a ranked city priority list.

```python
expansion_recommendation = pd.DataFrame({
    'City':                   city_expansion_metrics.index,
    'Revenue_per_Restaurant': city_expansion_metrics['Revenue_per_Restaurant'],
    'Expansion_Priority':     city_expansion_metrics['Expansion_Priority'],
    'Cuisine_Diversity':      cuisines_per_city,
    'Penetration_Rate':       penetration_analysis['Penetration_Rate_(%)'],
    'Growth_Potential':       penetration_analysis['Growth_Potential_(%)']
})

# Weighted Final Score: 40% Expansion Priority + 30% Growth Potential + 30% Revenue per Restaurant
expansion_recommendation['Final_Score'] = (
    expansion_recommendation['Expansion_Priority']      * 0.4 +
    expansion_recommendation['Growth_Potential']        * 0.3 +
    (expansion_recommendation['Revenue_per_Restaurant'] / expansion_recommendation['Revenue_per_Restaurant'].max() * 100) * 0.3
).round(0)

expansion_recommendation = expansion_recommendation.sort_values('Final_Score', ascending=False, ignore_index=True)
```

**Output — Top 3 Priority Cities:**

| Rank | City | Final Score | Revenue/Restaurant | Growth Potential |
|---|---|---|---|---|
| 🥇 1 | **Kolkata** | 80 | ₹4.04L | 99.9%+ |
| 🥈 2 | **Bangalore** | 80 | High | 99.87% |
| 🥉 3 | **Ahmedabad** | 79 | High | 99.95% |

**📊 Chart:**

![Final Expansion Priority Score](../Visuals/final_expansion_score.png)

>*Bar chart of the Final Expansion Priority Score for all 10 cities — higher score = better growth opportunity.*

### 💡 Key Insights

- **Kolkata Value Flip:** Despite lower AOV, Kolkata hits the highest Final Score (80) due to high revenue/restaurant (₹4.04L) and low saturation.
- **Ahmedabad "Gap" Play:** Highest-rated Tier-2 city with low penetration (0.05%) but high revenue-per-partner — "blank slate" growth potential.
- **Segmented Expansion Strategy for Jaipur/Lucknow:** Strategy must shift from "Quantity" to "Cuisine Filling" — address specific gaps from Section 8.3.

---

## 9️⃣. ✨Customer Experience Analysis

> **Business Challenge #7 — Questions Answered:**
> - What are preferred payment methods by demographic?
> - How do age groups/occupations behave differently?
> - What factors influence order value?
> - How can we personalize customer experience?
> - What drives customer satisfaction vs dissatisfaction?

---

### 9.1 Payment Method Analysis

**Goal:** Understand how customers pay and whether payment method affects order value.

```python
# Overall payment preferences
payment_analysis = delivered_orders.groupby('payment_method').agg({
    'order_id':     'count',
    'total_amount': ['sum', 'mean']
}).round(2)

payment_analysis['%_of_Orders']  = (payment_analysis['Orders'] / payment_analysis['Orders'].sum() * 100).round(1)
payment_analysis['%_of_Revenue'] = (payment_analysis['Total_Revenue'] / payment_analysis['Total_Revenue'].sum() * 100).round(1)

# Payment by age group
payment_by_age = delivered_orders.groupby(['age_group', 'payment_method']).size().unstack(fill_value=0)
payment_by_age_pct = (payment_by_age.div(payment_by_age.sum(axis=1), axis=0) * 100).round(1)

# Payment by city
payment_by_city = delivered_orders.groupby(['city', 'payment_method']).size().unstack(fill_value=0)
payment_by_city_pct = (payment_by_city.div(payment_by_city.sum(axis=1), axis=0) * 100).round(1)
```

**Output — Payment Preferences:**

| Payment Method | % of Orders | AOV |
|---|---|---|
| UPI | ~40% | ~₹695 |
| Credit Card | ~25% | ~₹695 |
| Debit Card | ~15% | ~₹695 |
| Net Banking | ~10% | ~₹695 |
| Cash on Delivery | ~10% | ~₹695 |

**📊 Chart:**

![Customer Payment Preferences](../Visuals/payment_preferences_donut.png)

>*Donut pie chart of payment method distribution across all orders (2022–2025).*

### 💡 Key Insights

- **The 90% Digital Floor:** 90% of orders are prepaid — drastically reducing "Return to Origin" risks and operational headaches.
- **The Trust Milestone:** At 10%, Swiggy's COD rate is far below the Indian e-commerce average (40–60%) — signals high platform trust.
- **The Great Equalizer:** UPI usage is identical across all age groups (18 to 56+) — UPI has crossed the "tech-savvy" barrier.
- **COD as Convenience, Not Budget:** COD users spend the same AOV (~₹695) as Credit Card users — COD is a "convenience/safety" choice, not a budget constraint.

---

### 9.2 Demographic Behavior Patterns

**Goal:** Examine how marital status and occupation influence ordering patterns and frequency.

```python
# Marital status impact
marital_behavior = delivered_orders.groupby('marital_status').agg({
    'order_id':     'count',
    'total_amount': ['mean', 'sum'],
    'user_id':      'nunique'
}).round(2)

marital_behavior['Orders_per_Customer'] = (marital_behavior['Orders'] / marital_behavior['Customers']).round(2)

# Occupation spending patterns
occupation_patterns = delivered_orders.groupby('occupation').agg({
    'order_id':     'count',
    'total_amount': ['mean', 'sum'],
    'user_id':      'nunique'
}).round(2)

occupation_patterns['Orders_per_Customer'] = (occupation_patterns['Orders'] / occupation_patterns['Customers']).round(2)
occupation_patterns = occupation_patterns.sort_values('Total_Revenue', ascending=False)
```

**Output:**

| Marital Status | Orders/Customer | AOV |
|---|---|---|
| Single | ~58 (higher) | ~₹694 |
| Married | ~56 | ~₹694 |

| Occupation | Frequency | Behaviour |
|---|---|---|
| Data Analyst | 63.64 (highest) | "Work Fuel" orderer |
| Software Engineer | ~63 | Daily Active User |
| Teacher/Architect/Accountant | 60+ | White-collar utility |

**📊 Chart:**

![Top 10 Occupations by Revenue](../Visuals/top_10_occupations_revenue.png)

>*Horizontal bar chart of top 10 occupations ranked by total revenue contribution.*

### 💡 Key Insights

- **The "Single" Engine:** Single customers place 17% more total orders and have higher frequency (58 orders/year) vs married.
- **The "Tech-Analytical" Powerhouse:** Software Engineers and Data Analysts — highest order frequency (~63 orders/customer).
- **AOV Stability:** Married users (likely larger households) have the same AOV (~₹694) as Singles — Married users are not yet using Swiggy for "Family Dinner."
- **Professional Precision:** Top 10 occupations in a very tight range — Swiggy is a "White-Collar Utility."

---

### 9.3 Order Value Influencers

**Goal:** Identify what characteristics (repeat status, ratings, time slot, age) are associated with higher order values.

```python
# Create order value categories
delivered_orders['order_value_category'] = pd.cut(
    delivered_orders['total_amount'],
    bins=[0, 300, 600, 1000, np.inf],
    labels=['Low (<300)', 'Medium (300-600)', 'High (600-1000)', 'Very High (>1000)']
)

# Key factors by value category
value_factors = delivered_orders.groupby('order_value_category').agg({
    'is_repeat_customer':  'mean',
    'order_id':            'count',
    'restaurant_rating':   'mean'
}).round(2)

value_factors.columns = ['Repeat_Customer_Rate', 'Order_Count', 'Avg_Restaurant_Rating']
value_factors['Repeat_Customer_Rate'] *= 100

# Time slot preference by age group
age_time_preference = delivered_orders.groupby(['age_group', 'time_slot']).size().unstack(fill_value=0)
age_time_pct = (age_time_preference.div(age_time_preference.sum(axis=1), axis=0) * 100).round(1)
```

**Output:**

| Order Value Category | Repeat Rate | Avg Restaurant Rating |
|---|---|---|
| Low (<₹300) | 100% | ~3.9 |
| Medium (₹300–₹600) | 100% | ~4.06 |
| High (₹600–₹1000) | 100% | ~4.10 |
| Very High (>₹1000) | 100% | **~4.15** |

### 💡 Key Insights

- **The 100% Loyalty Floor:** 100% repeat rate across all value categories — high-value spenders are recurring power users, not one-off splurge customers.
- **The Quality Premium:** Direct linear correlation between restaurant ratings and order value. Very High orders (>₹1000) come from restaurants rated 4.15+.
- **The 4.0 Barrier:** Customers appear hesitant to spend heavily below a 4.0 restaurant rating.
- **Age-Slot Consistency:** All age groups (18 to 56+) order at the same time slots — 87% concentrated in Lunch and Dinner — no demographic "offset" possible for load balancing.

---

### 9.4 Customer Journey — First vs Repeat Orders

**Goal:** Compare order behaviour between a customer's very first order and all subsequent repeat orders.

```python
first_orders         = delivered_orders.groupby('user_id')['order_date'].min().reset_index()
first_orders.columns = ['user_id', 'first_order_date']

delivered_with_first             = delivered_orders.merge(first_orders, on='user_id')
delivered_with_first['is_first_order'] = (delivered_with_first['order_date'] == delivered_with_first['first_order_date'])

journey_analysis = delivered_with_first.groupby('is_first_order').agg({
    'total_amount': 'mean',
    'order_id':     'count'
}).round(2)

journey_analysis.columns = ['Avg_Order_Value', 'Order_Count']
journey_analysis.index   = ['Repeat_Orders', 'First_Orders']
```

**Output:**

| Order Type | Count | AOV |
|---|---|---|
| First Orders | ~10,000 | **₹690** |
| Repeat Orders | ~5,60,000 | **₹695** |
| Difference | — | +0.7% |

**📊 Chart:**

![First vs Repeat AOV](../Visuals/first_vs_repeat_aov.png)

>*Bar chart comparing Average Order Value for First-Time orders vs Repeat orders.*

### 💡 Key Insights

- **The Trust-at-Entry Advantage:** First-time users spend ₹690 right away — this is a high-intent purchase, meaning Customer Acquisition Cost (CAC) is offset almost immediately.
- **The Reliability Plateau:** After the first order, AOV only grows by 0.7% — growth is driven by **Frequency, not by larger basket sizes**.
- **The "Golden First Mile":** Any delivery failure on that initial ₹690 order is a catastrophic LTV loss.
- **The Business is now a "Retention Machine":** 5.6 lakh repeat orders vs 10,000 first-time orders — focus must shift from "Finding New People" to "Finding New Occasions" for existing users.

---

### 9.5 Satisfaction Proxies

**Goal:** Use repeat customer rate as a proxy for satisfaction across restaurant types and rating buckets.

```python
# By restaurant type
satisfaction_by_restaurant_type = delivered_orders.groupby('restaurant_type').agg({
    'is_repeat_customer': 'mean',
    'total_amount':       'mean',
    'order_id':           'count'
}).round(2)
satisfaction_by_restaurant_type['Repeat_Rate'] = satisfaction_by_restaurant_type['is_repeat_customer'] * 100 * satisfaction_by_restaurant_type.columns

# By rating bucket
satisfaction_by_rating = delivered_orders.groupby('rating_bucket').agg({
    'is_repeat_customer': 'mean',
    'order_id':           'count'
}).round(2)

satisfaction_by_rating['Repeat_Rate'] = satisfaction_by_rating['is_repeat_customer'] * 100
```

**Output:**

| Rating Bucket | Repeat Rate | Orders |
|---|---|---|
| Excellent (4.5+) | 100% | High |
| Very Good (4.0–4.5) | 100% | High |
| Good (3.5–4.0) | 100% | High |
| Average (<3.5) | 100% | **43k (lowest volume)** |

**📊 Chart:**

![Repeat Rate by Rating Bucket](../Visuals/repeat_rate_by_rating.png)

>*Bar chart showing repeat customer rate (%) across each restaurant rating bucket.*

### 💡 Key Insights

- **"Excellent" + "Very Good" Volume:** These two buckets capture 44% of total volume — quality is the primary driver of high-frequency ordering.
- **The "Ecosystem Lock-in":** 100% repeat rate across all types suggests Swiggy One membership has reached a tipping point — customers default to Swiggy because fees are already paid.
- **The "Average" Stagnation:** Average-rated restaurants have the lowest order volume (43k). Even if customers repeat, they do so sparingly.
- **Cloud Kitchen Parity:** Cloud Kitchens have achieved AOV parity with Traditional restaurants — green light for Swiggy to further invest in private labels (like The Bowl Company).

---

## 🔟. 🚀Statistical Significance & Revenue Forecasting

### 10.1 Statistical Significance Test — Weekend vs Weekday AOV

**Goal:** Test whether the difference in Average Order Value between weekdays and weekends is statistically meaningful or just random variation.

```python
from scipy import stats

weekend_aov = delivered_orders[delivered_orders['day_type']=='Weekend']['total_amount']
weekday_aov = delivered_orders[delivered_orders['day_type']=='Weekday']['total_amount']

t_stat, p_value = stats.ttest_ind(weekend_aov, weekday_aov)

print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"Result: {'Statistically Significant' if p_value < 0.05 else 'Not Significant'}")
```

**Result:** The difference in Weekend vs Weekday AOV is **Not Statistically Significant** (p > 0.05).

**Interpretation:** Any small AOV differences between weekdays and weekends observed in the data are due to random noise, not a real behavioral difference. This confirms the earlier finding — customers spend the same amount regardless of the day.

---

### 10.2 Revenue Forecasting — Next 6 Months

**Goal:** Use Linear Regression to forecast monthly revenue for the next 6 months based on historical trends.

```python
from sklearn.linear_model import LinearRegression

monthly_revenue['month_num'] = range(len(monthly_revenue))
X = monthly_revenue[['month_num']].values
y = monthly_revenue['revenue'].values

model = LinearRegression()
model.fit(X, y)

future_months = np.array([[len(monthly_revenue) + i] for i in range(6)])
predictions   = model.predict(future_months)

for i, pred in enumerate(predictions, 1):
    print(f"Month +{i}: ₹{pred:,.2f}")
```

**How it works:**
1. Each historical month is assigned a sequential number (0, 1, 2 … 47 for 4 years).
2. A Linear Regression model learns the trend from this number → revenue relationship.
3. The model then predicts revenue for months 48 through 53 (next 6 months).

**Limitation:** Linear Regression captures the overall trend but not seasonality. The forecast reflects the current flat/slightly declining trend. Actual revenue will vary based on seasonality (e.g., July spike, February dip).

---

### 10.3 Industry Benchmark Comparison

```python
benchmarks = {
    'Metric':       ['Month 1 Retention', 'Cancellation Rate', 'Repeat Customer %', 'Avg Order Value'],
    'Swiggy':       ['26%',               '4.95%',             '100%',               '₹695'],
    'Industry Avg': ['35-40%',            '3-5%',              '60-70%',             '₹450-600'],
    'Status':       ['Below Average',     'Average',           'Exceptional',        'Above Average']
}
```

**Output:**

| Metric | Swiggy | Industry Avg | Status |
|---|---|---|---|
| Month 1 Retention | 26% | 35–40% | ⚠️ Below Average |
| Cancellation Rate | 4.95% | 3–5% | ✅ Average |
| Repeat Customer % | 100% | 60–70% | 🏆 Exceptional |
| Avg Order Value | ₹695 | ₹450–₹600 | ✅ Above Average |

---

## 1️⃣1️⃣. 🎯Strategic Recommendations

The following recommendations are generated programmatically from the data analysis results:

### 1. 👥Customer Retention Strategy

| Action | Detail |
|---|---|
| Focus segment | Champions (2,138 customers) |
| Re-engagement | 3,892 at-risk customers (90+ days inactive) |
| Loyalty program | Top 20% customers generating 84.1% of revenue |
| Revenue recovery potential | ₹2.87 Crores |

**Actions:**
- Launch tiered win-back campaigns (45/60/90-day triggers)
- Implement "3-Order Milestone" incentive for new users
- Create "Swiggy Black" VIP program for Champions segment

---

### 2. 💰Revenue Optimization

| Driver | Action |
|---|---|
| City | Defend Mumbai (₹8.76 Cr) + activate Ahmedabad/Lucknow |
| Cuisine | Cross-sell Beverages + promote Chinese (highest AOV ₹716) |
| Time | Launch "Afternoon Cravings" program (2–5 PM) |
| Month | "Off-Season" campaign for February to recover 12% dip |

---

### 3. 🏪Restaurant Partner Optimization

| Action | Detail |
|---|---|
| Support/train | ~100 underperforming restaurants |
| Revenue uplift potential | ₹1.08 Crores |
| Model expansion | Aggressively add Cloud Kitchens in Tier-2 cities |
| Quality floor | Monitor and coach restaurants rated below 3.5 |

---

### 4. 🍽️Menu & Product Strategy

| Action | Detail |
|---|---|
| Top items | Promote Paneer Burger + Cheese Burger combos |
| Cross-sell | Push Beverages + Desserts as add-ons |
| Price strategy | Focus on expanding ₹200–₹299 mid-range menu |
| Combos | Launch "Duo Deals" based on basket analysis top 20 pairs |

---

### 5. ⚡Operational Excellence

| Action | Target |
|---|---|
| Reduce cancellation rate | From 4.95% → < 3% |
| Revenue recovery | ₹25 Cr annual potential |
| Peak capacity | Increase Lunch/Dinner capacity by 761x baseline |
| High-cancellation city | Address Delhi (5.09%) urgently |

---

### 6. 🌍Market Expansion

| Priority | City | Score | Growth Potential |
|---|---|---|---|
| 1 | Kolkata | 80 | 99.9%+ |
| 2 | Bangalore | 80 | 99.87% |
| 3 | Ahmedabad | 79 | 99.95% |

**Cuisine Fill Initiative:** Recruit Biryani/Thai brands for Lucknow, and Beverages/Desserts/Healthy Food for Ahmedabad and Jaipur.

---

### 7. ✨Customer Experience Enhancement

| Action | Detail |
|---|---|
| Payment | Promote UPI (40%) — most popular, already dominant |
| Personalization | Target 26–35 age group and Software Engineers with occupation-specific offers |
| Quality | Improve experience at restaurants with rating < 3.5 |
| First order | Implement "New User Priority Dispatch" for flawless first experience |

---

### 💡 Expected Total Revenue Impact

| Source | Recovery/Growth |
|---|---|
| Cancellation reduction | ₹13 Crores |
| Customer retention | ₹5 Crores |
| Champions expansion | ₹8 Crores |
| Market expansion | ₹15 Crores |
| **Total Potential** | **₹40+ Crores** |

---

## 1️⃣2️⃣. 💼Executive Summary

### 📊 Key Business Metrics

| Metric | Value |
|---|---|
| Total Revenue (4 years) | ₹39.62 Crores |
| Total Orders | 6,00,000 |
| Delivered Orders | 5,70,281 (95.0%) |
| Cancelled Orders | 29,719 (4.95%) |
| Average Order Value | ₹695 |
| Unique Customers | 10,000 |
| Active Restaurants | 1,000 |
| Cities Covered | 10 |

---

### 🎯 Summary by Business Challenge

| Challenge | Key Finding | Priority |
|---|---|---|
| Customer Retention | 74% first-month churn; 3,892 at-risk customers | 🔴 HIGH |
| Revenue Optimization | Flat 0.1% YoY growth; February/off-peak underperformance | 🟠 MEDIUM |
| Restaurant Performance | 100 underperformers; ₹1.08 Cr opportunity | 🟠 MEDIUM |
| Menu & Product | Burger/Pizza duopoly; Dessert/Beverage cross-sell gap | 🟡 LOW-MEDIUM |
| Operational Efficiency | 4.95% cancellation = ₹25 Cr annual loss | 🔴 HIGH |
| Market Expansion | <0.1% penetration everywhere; Kolkata/Ahmedabad prioritized | 🟠 MEDIUM |
| Customer Experience | 90% digital payments; Data Analysts highest-frequency group | 🟡 LOW-MEDIUM |

---

### 🏆 Top 5 Strategic Priorities (Ranked by Revenue Impact)

**Priority 1 — Fix Cancellation Crisis** *(URGENT — 90 days)*
- Target: Reduce 4.95% → < 3%
- Impact: Save ₹13+ Crores annually
- Actions: Root cause analysis by city/restaurant; ETA improvements; quality interventions

**Priority 2 — Win Back At-Risk Customers** *(IMMEDIATE — 30 days)*
- Target: Re-engage 3,892 customers
- Impact: Recover ₹2.87 Crores
- Actions: Tiered win-back campaigns; personalized incentives; churn surveys

**Priority 3 — Improve Month 1 Retention** *(SHORT-TERM — 6 months)*
- Target: Increase 26% → 35%
- Impact: +₹5+ Crores annually
- Actions: Perfect first order experience; second-order incentive within 7 days

**Priority 4 — Expand Champions Program** *(MEDIUM-TERM — 12 months)*
- Target: Grow Champions from 21.4% → 30%
- Impact: +₹8+ Crores
- Actions: VIP benefits; exclusive access; milestone rewards ("Swiggy Black")

**Priority 5 — Strategic Market Expansion** *(LONG-TERM — 18 months)*
- Target: Enter Kolkata, Bangalore, Ahmedabad priority markets
- Impact: +₹15+ Crores
- Actions: Fill cuisine gaps; deepen city penetration; Cloud Kitchen onboarding

---

### 📈 Expected Impact (12 Months)

| Metric | Current | Target | Change |
|---|---|---|---|
| Annual Revenue | ₹39.62 Cr | ₹79+ Cr | +96% |
| Month 1 Retention | 26% | 35% | +9 pp |
| Cancellation Rate | 4.95% | <3% | -2 pp |
| Champions % | 21.4% | 30% | +8.6 pp |
| Market Penetration | ~0.05% | 0.2% | 4x |

---

### 💼 Investment Required

| Area | Investment |
|---|---|
| Technology (analytics, ML, app) | ₹2 Crores |
| Marketing (retention + acquisition) | ₹5 Crores |
| Operations (capacity + training) | ₹3 Crores |
| **Total** | **₹10 Crores** |
| **ROI** | **4x within 12 months** |

---

### 🚀 Monthly Success KPIs to Track

1. **Cancellation Rate** → Target: < 3%
2. **Month 1 Retention** → Target: > 35%
3. **At-Risk Recovery Rate** → Target: > 50%
4. **Champions % of Customer Base** → Target: > 25%
5. **Monthly Revenue Growth** → Target: > 15% MoM

---

> **Analysis Complete:** All 7 Business Challenges solved with data-driven insights, visualizations, and strategic recommendations.
>
> **Tool Stack Used:** Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, SciPy) + PostgreSQL
>
> **Documentation Purpose:** For reference and reproducibility by other analysts.

---

## 🧑‍💻 Author

**👤 Harsh Belekar**  
📍 Data Analyst | Python Developer | SQL | Power BI | Excel | Data Visualization  
📬 [LinkedIn](https://www.linkedin.com/in/harshbelekar) | 🔗[GitHub](https://github.com/Harsh-Belekar)

📧 [harshbelekar74@gmail.com](mailto:harshbelekar74@gmail.com)

---

⭐ *If you found this project helpful, feel free to star the repo and connect with me for collaboration!*
