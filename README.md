# Retail Data Warehouse Project

## Overview
This project implements a complete Business Intelligence data warehouse for retail analytics.

It includes:
- Data generation
- Data cleaning
- ETL pipeline
- Star schema modeling
- Analytical SQL queries
- Index optimization

---

## Architecture

Raw CSV → Clean Layer → Transform → PostgreSQL Warehouse → BI Queries

---

## Schema

Dimension Tables:
- dim_customer
- dim_product
- dim_time

Fact Table:
- fact_sales

---

## KPIs Implemented

- Total Revenue
- Revenue by Region
- Monthly Sales Trends
- Top 10 Products

---

## Tech Stack

- PostgreSQL
- Python (Pandas, SQLAlchemy)
- Faker
- Git

---

## How to Run

1. Run schema.sql
2. Generate raw data
3. Clean data
4. Run ETL load
5. Execute queries.sql