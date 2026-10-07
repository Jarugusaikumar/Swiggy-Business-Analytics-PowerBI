# Power BI Refresh Checklist

Use this checklist to refresh and validate the Power BI report locally.

## Before opening Power BI
- Confirm the repository is present locally.
- Confirm the CSV raw data files exist in `Data/raw`.
- Confirm the Power BI file exists at `powerbi/Swiggy_Business_Analytics.pbix`.
- Confirm Python dependencies are installed in the project virtual environment.
- Note: this project is designed to work in a CSV-first portfolio workflow without PostgreSQL.

## If using CSV files directly (default portfolio workflow)
1. Open Power BI Desktop.
2. Click `Get Data`.
3. Select `Text/CSV`.
4. Import the files from `Data/raw`:
   - users.csv
   - restaurants.csv
   - menu.csv
   - orders.csv
   - order_items.csv
5. In the Power Query Editor, rename columns to match the model if needed.
6. Set appropriate data types:
   - `user_id`, `restaurant_id`, `menu_id`, `order_id`, `order_item_id` -> Text
   - `age`, `quantity` -> Whole Number
   - `rating` -> Decimal Number
   - `order_date` -> Date
   - `delivery_time` -> Time
   - `total_amount`, `price` -> Decimal Number
7. Remove unnecessary columns if the report model does not need them.
8. Close & Apply.

## If using PostgreSQL (optional, advanced SQL demo)
1. Start PostgreSQL locally.
2. Confirm the `swiggy` database exists.
3. Open Power BI Desktop.
4. Click `Get Data` > `PostgreSQL database`.
5. Enter the server and database values.
6. Select the tables:
   - users
   - restaurants
   - menu
   - orders
   - order_items
7. Close & Apply.

This database route is optional and is recommended only when you explicitly want to showcase SQL/PostgreSQL skill in addition to the CSV-based portfolio workflow.

## Model validation
- Confirm the relationship model is star-schema friendly.
- Validate `orders` as the main fact table.
- Confirm `users`, `restaurants`, and `menu` are dimension tables.
- Check that relationship cardinality is correct.
- Make sure filter direction is single-direction where possible.
- Remove ambiguous or redundant relationships.

## DAX validation
- Confirm these core measures exist:
  - Total Orders
  - Total Revenue
  - Average Order Value
  - Total Customers
  - Cancellation Rate %
  - Orders per Customer
- Confirm measures behave correctly when slicers are applied.
- Check that card visuals and trend visuals update after refresh.

## Dashboard validation
Check each page visually:
- Executive Overview
- Customer Analytics
- Restaurant Analytics
- Revenue & Sales Analytics
- Business Insights
- Delivery / Operations analytics if included

Ensure:
- titles are consistent
- KPI cards update after filters
- no broken visuals or missing fields
- the data labels and legends are readable
- the report still looks clean after refreshing

## Final QA before sharing
- Validate the dataset matches the actual CSV file counts.
- Check that totals and KPI cards are consistent with the source data.
- Capture screenshots for GitHub.
- Save the final report version.
- Update the project README with the final report notes and screenshots.

## Final note
This checklist is designed for a portfolio project using synthetic data. It should be used to keep the report reproducible, polished, and recruiter-friendly without making false performance claims.
