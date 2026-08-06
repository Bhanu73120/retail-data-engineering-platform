# Retail Data Engineering Platform


[![Python CI](https://github.com/Bhanu73120/retail-data-engineering-platform/actions/workflows/python-app.yml/badge.svg)](https://github.com/Bhanu73120/retail-data-engineering-platform/actions/workflows/python-app.yml)


An end-to-end Retail Data Engineering project that implements a complete ETL pipeline using Python, Apache Airflow, MySQL, and GitHub Actions.

The pipeline automatically ingests retail order CSV files, validates and cleans the data, applies business rules, generates analytical summaries, and stores processed data into MySQL using the Medallion Architecture (Raw → Bronze → Silver → Gold).

---

# Project Architecture

```
                External CSV Files
                        │
                        ▼
              Airflow DAG Trigger
                        │
                        ▼
                Raw Data Ingestion
                        │
                        ▼
              Data Validation
                        │
                        ▼
            Customer & Product Cleaning
                        │
                        ▼
             Duplicate Removal
                        │
                        ▼
                 Bronze Layer
                        │
                        ▼
            Business Rule Processing
                        │
                        ▼
                 Silver Layer
                        │
                        ▼
          Sales Summary Generation
                        │
                        ▼
                  Gold Layer
                        │
                        ▼
                MySQL Data Warehouse
```


## Airflow DAG

![Airflow Graph](docs/images/airflow_graph.png)


## Successful Pipeline Run

![Airflow Success](docs/images/pipeline_summary.png)


## GitHub Actions

![Python CI](dashboards/screenshots/github_actions.png)


## Power BI Dashboard

![Power BI](dashboards/screenshots/powerbi_dashboard.png)

## Power BI Dashboard By Product

![Power BI](dashboards/screenshots/dashboard_overview_by_product.png)

---

# Features

- Automated ETL Pipeline using Apache Airflow
- Dynamic Batch ID generation
- Source file tracking
- Ingestion timestamp tracking
- Raw → Bronze → Silver → Gold architecture
- Data validation before and after cleaning
- Customer data cleaning
- Product data cleaning
- Duplicate removal
- Business rule implementation
- Sales summary generation
- MySQL data warehouse loading
- Structured logging
- Unit testing using Pytest
- Code coverage using pytest-cov
- Continuous Integration using GitHub Actions

---

# Tech Stack

- Python 3.11
- Apache Airflow 2.10
- MySQL
- Pandas
- NumPy
- Pytest
- Git
- GitHub
- GitHub Actions

---

# Project Structure

```
retail-data-engineering-platform
│
├── airflow/
│   └── dags/
│       └── retail_pipeline_dag.py
│
├── config/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── dashboards/
│   ├── powerbi/
│   └── screenshots/
│
├── docs/
│
├── scripts/
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── validation/
│   ├── warehouse/
│   └── utils/
│
├── sql/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# ETL Pipeline

## Raw Layer

- Reads retail CSV files
- Generates Batch ID
- Stores source filename
- Stores ingestion timestamp

---

## Bronze Layer

- Validates input data
- Removes duplicate records
- Cleans customer names
- Cleans product names

---

## Silver Layer

Applies business rules:

- Price Category
- Discount
- Final Price

---

## Gold Layer

Generates analytical metrics:

- Total Revenue
- Total Orders
- Average Order Value
- Highest Order Value
- Lowest Order Value

---

# MySQL Tables

The pipeline loads processed data into three tables.

## orders

Stores cleaned Bronze layer data.

## orders_silver

Stores business-rule enriched Silver layer data.

## sales_summary

Stores Gold layer analytical metrics.

Each batch includes:

- Batch ID
- Source File
- Ingestion Timestamp

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/Bhanu73120/retail-data-engineering-platform.git
```

---

## Move into Project

```bash
cd retail-data-engineering-platform
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Airflow

Configure:

- Airflow Variables
- MySQL Connection

Place CSV files into:

```
External_CSVs/incoming/
```

Run the DAG:

```
retail_data_pipeline
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run with coverage

```bash
python -m pytest --cov=src
```

---

# Continuous Integration

GitHub Actions automatically runs:

- Dependency installation
- Unit tests
- Code coverage

Every push to the `main` branch is automatically validated.

---

# Project Documentation

Detailed setup guides are available inside the `docs` folder.

- project_overview.md
- airflow_setup.md
- mysql_setup.md
- pipeline_execution.md

---

# Dashboard

Power BI dashboard is available in:

```
dashboards/powerbi/
```

Pipeline screenshots are available in:

```
dashboards/screenshots/
```

---

# Project Status

- ✅ Raw Layer
- ✅ Bronze Layer
- ✅ Silver Layer
- ✅ Gold Layer
- ✅ Apache Airflow
- ✅ MySQL Integration
- ✅ Batch Metadata Tracking
- ✅ Source File Tracking
- ✅ Ingestion Timestamp Tracking
- ✅ Unit Testing
- ✅ GitHub Actions CI Passing

---

# Author

**Bhanu Prakash**

GitHub:

https://github.com/Bhanu73120