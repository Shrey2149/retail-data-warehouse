-- =========================================
-- Retail Data Warehouse Schema
-- =========================================

-- Drop tables if they exist (for development reset)
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;

-- =========================================
-- Dimension: Product
-- =========================================
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2) NOT NULL
);

-- =========================================
-- Dimension: Customer
-- =========================================
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    state VARCHAR(50),
    join_date DATE,
    segment VARCHAR(50)
);

-- =========================================
-- Fact Table: Sales
-- =========================================
CREATE TABLE fact_sales (
    transaction_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    transaction_date DATE NOT NULL,

    -- Foreign Keys
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id)
);

-- =========================================
-- Indexes for Performance
-- =========================================
CREATE INDEX idx_fact_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_product ON fact_sales(product_id);
CREATE INDEX idx_fact_date ON fact_sales(transaction_date);