# Retail Data Engineering Platform - Project Overview

## Introduction

The Retail Data Engineering Platform is an end-to-end ETL pipeline developed using Python, Apache Airflow, and MySQL.

The project follows the Medallion Architecture (Raw → Bronze → Silver → Gold) to process retail order data through multiple transformation stages while maintaining data quality, traceability, and batch-level metadata.

Each pipeline execution processes one incoming CSV file, assigns a unique Batch ID, loads data into MySQL, and generates aggregated business metrics.

---

## Project Architecture

```
Incoming CSV
      │
      ▼
 Raw Layer
      │
      ▼
 Bronze Layer
(Data Cleaning)
      │
      ▼
 Bronze MySQL Table
      │
      ▼
 Silver Layer
(Business Rules)
      │
      ▼
 Silver MySQL Table
      │
      ▼
 Gold Layer
(Sales Summary)
      │
      ▼
Sales Summary MySQL Table
```

---

## Medallion Architecture

### Raw Layer

- Receives external CSV files
- Generates Batch ID
- Preserves original data

### Bronze Layer

- Removes duplicate records
- Cleans customer names
- Cleans product names
- Validates cleaned data

### Silver Layer

- Applies business rules
- Categorizes products by price
- Calculates discounts
- Calculates final selling price

### Gold Layer

- Generates business metrics
- Total Revenue
- Total Orders
- Average Order Value
- Highest Order Value
- Lowest Order Value

---

## Technologies Used

| Component | Technology |
|------------|------------|
| Language | Python 3.11 |
| Workflow Orchestration | Apache Airflow |
| Database | MySQL |
| Data Processing | Pandas |
| Numerical Operations | NumPy |
| Testing | Pytest |
| CI | GitHub Actions |
| Version Control | Git & GitHub |

---

## Key Features

- End-to-End ETL Pipeline
- Dynamic Batch Processing
- Data Validation
- Data Cleaning
- Duplicate Removal
- Business Rule Implementation
- Automated Sales Summary Generation
- MySQL Integration
- Apache Airflow Orchestration
- Batch Tracking
- Unit Testing
- GitHub Actions Continuous Integration

---

## Output Tables

The pipeline loads processed data into three MySQL tables.

- orders
- orders_silver
- sales_summary

Each execution is traceable using:

- Batch ID
- Source File
- Ingestion Timestamp

---

## Project Outcome

The project demonstrates how a modern data engineering pipeline can automate data ingestion, transformation, validation, warehouse loading, and reporting using Apache Airflow and MySQL.