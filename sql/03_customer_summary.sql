USE ecommerce_dw;

SET hive.auto.convert.join=false;
SET hive.execution.engine=mr;

INSERT OVERWRITE TABLE customer_order_summary
SELECT
    c.customer_id,
    c.name,
    SUM(o.amount) AS total_spent,
    COUNT(o.order_id) AS total_orders
FROM orders_transformed o
JOIN customers_raw c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.name;
