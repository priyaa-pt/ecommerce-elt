from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


HIVE_HOME = "/mnt/E/BigData-Tools/Hive"
HADOOP_HOME = "/mnt/E/BigData-Tools/Hadoop"

ENV = {
    "HIVE_HOME": HIVE_HOME,
    "HADOOP_HOME": HADOOP_HOME,
    "PATH": f"{HIVE_HOME}/bin:{HADOOP_HOME}/bin:{HADOOP_HOME}/sbin:/usr/local/bin:/usr/bin:/bin",
}


with DAG(
    dag_id="ecommerce_elt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "elt", "hive"],
) as dag:

    check_hdfs = BashOperator(
        task_id="check_hdfs",
        bash_command="""
        echo "Checking existing HDFS data..."
        hdfs dfs -ls /data/raw/orders
        hdfs dfs -ls /data/raw/customers
        """,
        env=ENV,
    )

    transform_orders = BashOperator(
        task_id="transform_orders",
        bash_command="""
        beeline -u jdbc:hive2://localhost:10000 -e "
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
        "
        """,
        env=ENV,
    )

    customer_summary = BashOperator(
        task_id="customer_summary",
        bash_command="""
        beeline -u jdbc:hive2://localhost:10000 -e "
        USE ecommerce_dw;
        SET hive.auto.convert.join=false;
        SET hive.execution.engine=mr;

        INSERT OVERWRITE TABLE customer_order_summary
        SELECT
            c.customer_id,
            c.name,
            SUM(o.amount),
            COUNT(o.order_id)
        FROM orders_transformed o
        JOIN customers_raw c
          ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name;
        "
        """,
        env=ENV,
    )

    daily_sales = BashOperator(
        task_id="daily_sales",
        bash_command="""
        beeline -u jdbc:hive2://localhost:10000 -e "
        USE ecommerce_dw;

        INSERT OVERWRITE TABLE daily_sales_summary
        SELECT
            order_date,
            SUM(amount),
            COUNT(order_id)
        FROM orders_transformed
        GROUP BY order_date;
        "
        """,
        env=ENV,
    )

    top_customers = BashOperator(
        task_id="top_customers",
        bash_command="""
        beeline -u jdbc:hive2://localhost:10000 -e "
        USE ecommerce_dw;

        SELECT
            customer_id,
            name,
            total_spent,
            total_orders
        FROM customer_order_summary
        ORDER BY total_spent DESC
        LIMIT 3;
        "
        """,
        env=ENV,
    )

    check_hdfs >> transform_orders
    transform_orders >> [customer_summary, daily_sales]
    customer_summary >> top_customers
