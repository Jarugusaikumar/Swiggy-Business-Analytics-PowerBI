# Data Model

## Conceptual architecture
The project follows a star-schema structure where the order-level transaction table is the primary fact table and the customer, restaurant, and item dimensions support analysis.

## Fact table
### orders
- Primary fact table
- Each row represents one order
- Business KPIs such as revenue, order count, and cancellation rate are calculated from this table

## Dimension tables
### users
- Customer attributes
- Supports segmentation, repeat-purchase, and user-level analysis

### restaurants
- Restaurant attributes such as city, cuisine, rating, and kitchen type
- Supports city and restaurant performance analysis

### menu
- Product catalog data used to analyze item categories and menu mix

## Relationship summary
- orders.user_id -> users.user_id
- orders.restaurant_id -> restaurants.restaurant_id
- menu.restaurant_id -> restaurants.restaurant_id
- order_items.order_id -> orders.order_id
- order_items.menu_id -> menu.menu_id

## Analytical design guidance
- Keep the fact table at the center of the model.
- Use dimensions for slicing and filtering by customer, restaurant, and item attributes.
- Avoid ambiguous multi-path relationships and unnecessary snowflaking.
- In Power BI, favor single-direction filters from dimensions to the fact table.

## Portfolio recommendation
This model is suitable for dashboarding, KPI calculation, and business analysis. It also maps cleanly to a modern Power BI star schema.
