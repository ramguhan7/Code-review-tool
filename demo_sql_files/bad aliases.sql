SELECT
    order_id,
    amount as amt
FROM orders
JOIN customers ON orders.customer_id = customers.id
