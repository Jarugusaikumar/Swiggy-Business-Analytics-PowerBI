"""Simple data quality checks for the Swiggy dataset."""

from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[2]
data_dir = root / 'data' / 'raw'

files = [
    'users.csv',
    'restaurants.csv',
    'menu.csv',
    'orders.csv',
    'order_items.csv',
]

print('Swiggy data quality checks')
print('=' * 40)

for file_name in files:
    path = data_dir / file_name
    df = pd.read_csv(path)
    print(f'{file_name}: rows={len(df)}; columns={list(df.columns)}')
    print(f'  missing_values={int(df.isna().sum().sum())}')
    print(f'  duplicate_rows={int(df.duplicated().sum())}')
    print()

orders = pd.read_csv(data_dir / 'orders.csv')
print('Status distribution:')
print(orders['order_status'].value_counts().to_string())
print()
print('Revenue summary:')
print(orders['total_amount'].describe().to_string())
