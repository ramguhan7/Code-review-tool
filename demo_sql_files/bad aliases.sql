SELECT
    order,
    amount as amt,
    NULL AS Dummycolumn --why this
FROM orders o
JOIN customers c ON o.customer_id = c.id --join needed
JOIN patients p on o.patienid = p.id 
