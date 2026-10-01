USE ecommerce_dw;

SELECT
    customer_id,
    name,
    ROUND(total_spent, 2) AS total_spent,
    total_orders
FROM customer_order_summary
ORDER BY total_spent DESC
LIMIT 10;
