SELECT
    order_id,
    amount as amt,
    NULL AS Dummycolumn
FROM orders o
JOIN customers c ON o.customer_id = c.id --join needed
JOIN patients p on o.patienid = p.id
