-- Replace your-project-id with your actual project id

CREATE SCHEMA IF NOT EXISTS `your-project-id.cpg_retail`;

CREATE TABLE IF NOT EXISTS `your-project-id.cpg_retail.dim_store` (
  store_id STRING,
  store_name STRING,
  city STRING,
  region STRING
);

CREATE TABLE IF NOT EXISTS `your-project-id.cpg_retail.dim_sku` (
  sku_id STRING,
  sku_name STRING,
  category STRING,
  brand STRING
);

CREATE TABLE IF NOT EXISTS `your-project-id.cpg_retail.dim_date` (
  date_id DATE,
  year INT64,
  month INT64,
  day INT64
);

CREATE TABLE IF NOT EXISTS `your-project-id.cpg_retail.fact_sales` (
  sale_date DATE,
  store_id STRING,
  sku_id STRING,
  units_sold INT64,
  net_sales FLOAT64,
  promo_flag BOOL
);
