# Data Dictionary

## Source tables

### users
| Column | Type | Description |
|---|---|---|
| user_id | string | Unique user identifier |
| user_name | string | Full name of the customer |
| age | integer | Customer age |
| gender | string | Male or Female |
| marital_status | string | Marital status |
| occupation | string | Customer occupation |

### restaurants
| Column | Type | Description |
|---|---|---|
| restaurant_id | string | Unique restaurant identifier |
| restaurant_name | string | Restaurant name |
| city | string | Restaurant city |
| cuisine | string | Primary cuisine type |
| rating | float | Restaurant rating |
| is_cloud_kitchen | integer | Flag for cloud kitchen model |

### menu
| Column | Type | Description |
|---|---|---|
| menu_id | string | Unique menu item identifier |
| restaurant_id | string | Linked restaurant |
| item_name | string | Menu item name |
| category | string | Item category |
| price | decimal | Item price |
| is_veg | integer | Vegetarian flag |

### orders
| Column | Type | Description |
|---|---|---|
| order_id | string | Unique order number |
| user_id | string | Customer who placed the order |
| restaurant_id | string | Restaurant associated with the order |
| order_date | date | Date of order |
| delivery_time | time | Order time-of-day |
| order_status | string | Delivered or Cancelled |
| payment_method | string | Payment type |
| total_amount | decimal | Total order revenue |

### order_items
| Column | Type | Description |
|---|---|---|
| order_item_id | string | Order line item identifier |
| order_id | string | Parent order |
| menu_id | string | Product sold |
| quantity | integer | Quantity purchased |
| price | decimal | Unit price or line amount |

## Derived fields used in analysis
- City revenue contribution
- Revenue by cuisine
- Cancellation rate
- Customer order frequency
- Restaurant performance score

## Data quality notes
- The data is synthetic and generated for educational use.
- Order status is limited to Delivered and Cancelled.
- Actual delivery duration and driver metrics are not included in the source files.
