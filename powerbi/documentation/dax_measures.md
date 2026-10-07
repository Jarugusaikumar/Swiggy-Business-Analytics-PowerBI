# Recommended DAX measures

## Core measures
```DAX
Total Orders = COUNTROWS(orders)

Total Revenue = SUM(orders[total_amount])

Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Total Customers = DISTINCTCOUNT(orders[user_id])

Cancellation Rate % = DIVIDE(
    CALCULATE(COUNTROWS(orders), orders[order_status] = "Cancelled"),
    [Total Orders],
    0
)

Orders per Customer = DIVIDE([Total Orders], [Total Customers], 0)

Customer Revenue = CALCULATE([Total Revenue], ALLEXCEPT(orders, orders[user_id]))
```

## Trend measures
```DAX
Revenue Growth % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = CALCULATE([Total Revenue], DATEADD('DateTable'[Date], -1, YEAR))
RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue, 0)
```

## Notes
- Only create measures that match the actual data model.
- Do not use delivery-duration metrics unless the source data includes actual timestamps for pickup and completion.
- Keep measure names clean and consistent for recruiter-facing portfolio dashboards.
