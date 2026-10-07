"""CSV-first analytics pipeline for the Swiggy portfolio project.

This script keeps the project runnable without PostgreSQL by validating the raw CSV
source files, calculating business KPIs, and saving processed outputs for dashboarding.
"""

from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[2]
raw_dir = root / 'Data' / 'raw'
processed_dir = root / 'data' / 'processed'
processed_dir.mkdir(parents=True, exist_ok=True)

required_files = [
    'users.csv',
    'restaurants.csv',
    'menu.csv',
    'orders.csv',
    'order_items.csv',
]

missing = [file_name for file_name in required_files if not (raw_dir / file_name).exists()]
if missing:
    raise FileNotFoundError(f'Missing CSV files: {missing}')

users = pd.read_csv(raw_dir / 'users.csv')
restaurants = pd.read_csv(raw_dir / 'restaurants.csv')
menu = pd.read_csv(raw_dir / 'menu.csv')
orders = pd.read_csv(raw_dir / 'orders.csv')
order_items = pd.read_csv(raw_dir / 'order_items.csv')

print('Swiggy CSV-first data pipeline')
print('=' * 50)
print(f'Users rows: {len(users):,}')
print(f'Restaurants rows: {len(restaurants):,}')
print(f'Menu rows: {len(menu):,}')
print(f'Orders rows: {len(orders):,}')
print(f'Order items rows: {len(order_items):,}')
print()
print('Data quality check:')
for label, df in [('users', users), ('restaurants', restaurants), ('menu', menu), ('orders', orders), ('order_items', order_items)]:
    print(f'- {label}: missing={int(df.isna().sum().sum())}, duplicates={int(df.duplicated().sum())}')

city_revenue = (
    orders.merge(restaurants[['restaurant_id', 'city']], on='restaurant_id', how='left')
    .groupby('city', as_index=False)['total_amount']
    .sum()
    .sort_values('total_amount', ascending=False)
    .rename(columns={'total_amount': 'revenue_inr'})
)
city_revenue.to_csv(processed_dir / 'city_revenue.csv', index=False)

customer_revenue = (
    orders.groupby('user_id', as_index=False)['total_amount']
    .sum()
    .sort_values('total_amount', ascending=False)
    .rename(columns={'total_amount': 'customer_revenue_inr'})
)
customer_revenue.to_csv(processed_dir / 'customer_revenue.csv', index=False)

summary = {
    'total_orders': int(len(orders)),
    'total_revenue_inr': float(orders['total_amount'].sum()),
    'avg_order_value_inr': float(orders['total_amount'].mean()),
    'distinct_customers': int(orders['user_id'].nunique()),
    'cancellation_rate_pct': float(orders['order_status'].eq('Cancelled').mean() * 100),
    'top_city_revenue_inr': float(city_revenue['revenue_inr'].iloc[0]),
    'top_city_name': str(city_revenue['city'].iloc[0]),
}

pd.DataFrame([summary]).to_csv(processed_dir / 'key_metrics.csv', index=False)

print()
print('Key metrics:')
for key, value in summary.items():
    print(f'- {key}: {value}')

print()
print(f'Processed outputs saved to: {processed_dir}')
