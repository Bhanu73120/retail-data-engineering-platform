# Retail Data Engineering Platform
[![Python CI](https://github.com/Bhanu73120/retail-data-engineering-platform/actions/workflows/python-app.yml/badge.svg)](https://github.com/Bhanu73120/retail-data-engineering-platform/actions/workflows/python-app.yml)


## Project Overview

The Retail Data Engineering Platform is an end-to-end ETL (Extract, Transform, Load) pipeline built using Python. The project processes raw retail order data through multiple stages, including data validation, cleaning, transformation, and analytical reporting.

The pipeline follows the Medallion Architecture (Raw → Bronze → Silver → Gold), which is widely used in modern Data Engineering projects. The project also includes automated unit testing, logging, and Continuous Integration (CI) using GitHub Actions to ensure code quality and reliability.

---

##  Architecture

                Raw Orders CSV
                      │
                      ▼
              Data Ingestion
                      │
                      ▼
        Validate Required Columns
        Validate Data Types
                      │
                      ▼
          Clean Customer Data
          Clean Product Data
          Remove Duplicates
                      │
                      ▼
               Bronze Layer
                      │
                      ▼
          Validate Cleaned Data
                      │
                      ▼
          Apply Business Rules
        • Price Category
        • Discount
        • Final Price
                      │
                      ▼
               Silver Layer
                      │
                      ▼
         Generate Sales Summary
                      │
                      ▼
                Gold Layer

##  Features

- End-to-End ETL Pipeline
- Data Validation
- Data Cleaning
- Duplicate Removal
- Business Rule Implementation
- Sales Summary Generation
- Structured Logging
- Unit Testing using Pytest
- Code Coverage using pytest-cov
- Continuous Integration using GitHub Actions


##  Tech Stack

- Python 3.11
- Pandas
- NumPy
- Pytest
- Pytest-Cov
- Git
- GitHub
- GitHub Actions


##  Project Structure

retail-data-engineering-platform
│
├── config/
│   └── config.py
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── scripts/
│   ├── download_data.py
│   ├── raw_to_bronze.py
│   ├── bronze_to_silver.py
│   └── silver_to_gold.py
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── warehouse/
│   └── utils/
│
├── tests/
│
├── requirements.txt
│
└── README.md


##  How to Run

### Clone the Repository

```bash
git clone https://github.com/Bhanu73120/retail-data-engineering-platform.git
```

### Navigate to the Project

```bash
cd retail-data-engineering-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Execute the ETL Pipeline

```bash
python -m scripts.download_data

python -m scripts.raw_to_bronze

python -m scripts.bronze_to_silver

python -m scripts.silver_to_gold
```

---

## ✅ Running Unit Tests

Run all unit tests

```bash
pytest
```

Run tests with code coverage

```bash
python -m pytest --cov=src --cov-report=html
```

Open the HTML coverage report

**Windows**

```bash
start htmlcov/index.html
```

---

## ⚙️ Continuous Integration

This project uses **GitHub Actions** for Continuous Integration.

Whenever code is pushed to the **main** branch:

- A fresh Ubuntu runner is created
- Python is installed
- Project dependencies are installed
- All unit tests are executed automatically
- The workflow reports Success or Failure


##  Current Project Status

- ✔ Raw Layer Implemented
- ✔ Bronze Layer Implemented
- ✔ Silver Layer Implemented
- ✔ Gold Layer Implemented
- ✔ Data Validation
- ✔ Data Cleaning
- ✔ Business Rules
- ✔ Logging
- ✔ Unit Testing
- ✔ Code Coverage
- ✔ GitHub Actions CI


##  Future Improvements

- Docker
- Apache Airflow
- Azure Data Factory
- Azure Data Lake Storage
- Databricks
- Snowflake
- Power BI Dashboard
- CI/CD Deployment

---

##  Author

**Bhanu Prakash**

GitHub: https://github.com/Bhanu73120