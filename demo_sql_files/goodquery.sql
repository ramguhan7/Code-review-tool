/****************************************************************************************************************
Entity Name: pefect file 
Author: RGG
Description: SQL has the all standards followed 
*****************************************************************************************************************/
WITH CTE AS (
SELECT
     c.id AS CustomerID
    ,COUNT(DISTINCT o.order_id) AS TotalOrderCNT
    ,SUM(o.amount) AS TotalAMT
FROM orders o
JOIN customers c
ON orders.customer_id = customers.id
JOIN shca_source_data.LAwson.APENVAST lawson
ON c.id = LAWSON.id --may need to remove this join in future
GROUP BY c.id --group by needed
)

SELECT  * FROM CTE 