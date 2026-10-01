USE ecommerce_dw;

INSERT OVERWRITE TABLE orders_transformed
SELECT
    order_id,
    customer_id,
    CAST(amount AS DOUBLE),
    CAST(order_date AS DATE)
FROM orders_raw
WHERE order_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND CAST(amount AS DOUBLE) IS NOT NULL
  AND CAST(order_date AS DATE) IS NOT NULL;
