# Power BI Page Plan

## Executive Overview
- Total Orders
- Total Revenue
- Average Order Value
- Total Customers
- Cancellation Rate
- Monthly Revenue Trend
- Revenue by City
- Revenue by Restaurant

## Customer Analytics
- New vs Returning Customers
- Customer Segmentation
- Orders per Customer
- Customer Revenue
- Top Customers
- Retention indicators (if repeat-order logic is added)

## Restaurant Analytics
- Top Restaurants
- Restaurant Revenue
- Restaurant Order Volume
- City-wise restaurant performance
- Ratings where available

## Delivery Analytics
- Average Delivery Time (only if order timestamps support duration logic)
- Delayed orders (requires event-level delivery data)
- City-wise delivery performance
- Cancellation analysis

## Revenue & Sales Analytics
- Revenue Trend
- Revenue by City
- Revenue by Restaurant
- Revenue by Cuisine
- Average Order Value
- Growth %

## Business Insights
Each card should show:
- Business observation
- Supporting KPI
- Possible business reason
- Recommended action

## Data notes
The current synthetic dataset supports order-level, customer-level, and restaurant-level analytics well. Actual delivery duration metrics require a separate event table with pickup and drop timestamps.
