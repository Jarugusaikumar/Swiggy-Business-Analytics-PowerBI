"""Portfolio-friendly EDA summary for the Swiggy synthetic dataset."""

from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[2]
data_dir = root / 'data' / 'raw'

orders = pd.read_csv(data_dir / 'orders.csv')
restaurants = pd.read_csv(data_dir / 'restaurants.csv')
users = pd.read_csv(data_dir / 'users.csv')

print('Swiggy Business & Operations Analytics - EDA Summary')
print('=' * 60)
print(f'Total orders: {len(orders):,}')
print(f'Total revenue: INR {orders["total_amount"].sum():,.2f}')
print(f'Average order value: INR {orders["total_amount"].mean():,.2f}')
print(f'Distinct customers: {orders["user_id"].nunique():,}')
print(f'Cancellation rate: {orders["order_status"].eq("Cancelled").mean() * 100:.2f}%')
print()

city_revenue = (
    orders.merge(restaurants[['restaurant_id', 'city']], on='restaurant_id', how='left')
    .groupby('city', as_index=False)['total_amount']
    .sum()
    .sort_values('total_amount', ascending=False)
)
print('Top 5 cities by revenue:')
print(city_revenue.head().to_string(index=False))
print()

print('Top 5 customers by revenue:')
customer_revenue = orders.groupby('user_id', as_index=False)['total_amount'].sum().sort_values('total_amount', ascending=False)
print(customer_revenue.head().to_string(index=False))
print()
print('Order status mix:')
print(orders['order_status'].value_counts().to_string())
