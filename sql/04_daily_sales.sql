USE ecommerce_dw;

INSERT OVERWRITE TABLE daily_sales_summary
SELECT
    order_date,
    SUM(amount) AS total_sales,
    COUNT(order_id) AS total_orders
FROM orders_transformed
GROUP BY order_date;
