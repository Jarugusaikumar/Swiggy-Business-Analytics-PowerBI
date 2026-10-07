# Business Requirements

## Project context
This project frames a food-delivery business as a portfolio-ready analytics case study. The goal is to convert raw order, customer, restaurant, and item-level transaction data into actionable business insights for revenue, customer, and operations analysis.

## Core business questions
1. Which cities generate the most revenue and order volume?
2. Which restaurants perform best by revenue, rating, and order volume?
3. How do order trends vary by time-of-day, city, and payment method?
4. Which customer segments drive the highest revenue?
5. What proportion of orders are cancelled, and which conditions likely influence cancellations?
6. Which products or menu categories are most frequently purchased?
7. Where should the business invest to improve revenue, retention, and operational flow?

## Stakeholder lens
- Executive leadership: revenue trends, market potential, operational health
- Operations team: cancellation patterns, delivery timing, service performance
- Marketing team: customer segmentation and repeat-order behavior
- Restaurant partners: performance, city-level demand, rating and sales trends

## KPI definitions
The data supports the following measures:
- Total Orders
- Total Revenue
- Average Order Value
- Total Customers
- Cancellation Rate
- City revenue contribution
- Restaurant revenue contribution
- Payment method mix
- Order status mix

## Data limitations
Some business metrics such as actual delivery duration, route optimization, and driver performance require more granular operational data than the current synthetic dataset contains. The dataset includes order time-of-day and status fields, but not actual ETA, driver ID, or trip-level performance logs.

## Portfolio focus
The objective is not to claim real business performance; it is to demonstrate analytical reasoning on a realistic synthetic food-delivery dataset using Python, SQL, and Power BI.
