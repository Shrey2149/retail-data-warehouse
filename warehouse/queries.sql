-- =========================================
-- Retail BI Analytical Queries
-- =========================================

-- 1️⃣ Total Revenue
SELECT SUM(total_amount) AS total_revenue
FROM fact_sales;



-- 2️⃣ Revenue by Region
-- (Assumes region column exists in dim_customer or separate region table)
-- If region is in dim_customer:

SELECT dc.state AS region,
       SUM(fs.total_amount) AS revenue
FROM fact_sales fs
JOIN dim_customer dc
  ON fs.customer_id = dc.customer_id
GROUP BY dc.state
ORDER BY revenue DESC;



-- 3️⃣ Monthly Sales
SELECT dt.year,
       dt.month,
       SUM(fs.total_amount) AS monthly_revenue
FROM fact_sales fs
JOIN dim_time dt
  ON fs.date_id = dt.date_id
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month;



-- 4️⃣ Top 10 Products by Revenue
SELECT dp.name,
       SUM(fs.total_amount) AS total_revenue
FROM fact_sales fs
JOIN dim_product dp
  ON fs.product_id = dp.product_id
GROUP BY dp.name
ORDER BY total_revenue DESC
LIMIT 10;