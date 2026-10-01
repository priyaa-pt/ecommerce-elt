# E-Commerce ELT Pipeline using Hadoop, Hive and Airflow

## Overview

This project implements an end-to-end E-Commerce ELT pipeline using
Hadoop HDFS, Apache Hive, Sqoop and Apache Airflow.

The pipeline ingests customer and order data, stores raw data in HDFS,
transforms it using Hive, performs data quality checks and generates
business analytics.

## Architecture

MySQL / CSV Data
        |
        v
      Sqoop
        |
        v
      HDFS
        |
        v
   Hive RAW Tables
        |
        v
Hive Transformations
        |
        +------------------+
        |                  |
        v                  v
Customer Summary     Daily Sales
        |
        v
   Top Customers
        |
        v
   Business Report

Airflow orchestrates the pipeline.

## Technologies

- Linux
- Hadoop 3.3.6
- HDFS
- Apache Hive 4.0.1
- Apache Sqoop 1.4.7
- Apache Airflow 3.3.2
- Java
- SQL
- Git/GitHub

## Project Structure

```text
ecommerce-elt/
├── airflow/
│   └── dags/
│       └── ecommerce_elt_pipeline.py
├── input/
│   └── orders.csv
├── sql/
│   ├── 01_create_raw_tables.sql
│   ├── 02_transform.sql
│   ├── 03_customer_summary.sql
│   ├── 04_daily_sales.sql
│   └── 05_top_customers.sql
├── customers.java
├── .gitignore
└── README.md

