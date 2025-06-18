SELECT
     c.id AS CustomerID
    ,COUNT(DISTINCT o.order_id) AS TotalOrderCNT
    ,SUM(o.amount) AS TotalAMT
FROM orders o
JOIN customers c
ON orders.customer_id = customers.id --may need to remove this join in future
GROUP BY c.id