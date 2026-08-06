# Apache Airflow Setup

## Overview

Apache Airflow is used to orchestrate the complete ETL pipeline. Each DAG run processes one incoming CSV file from the external folder and loads the processed data into MySQL.

---

## Airflow Variables

The following Airflow Variables must be configured.

| Variable | Description |
|-----------|-------------|
| PROJECT_PATH | Path to the Retail Data Engineering Platform project |
| EXTERNAL_FOLDER_PATH | Path containing incoming and processed CSV files |

---

## Airflow Connection

Create a MySQL connection named:

```
retail_mysql
```

Connection Type

```
MySQL
```

Configure the following:

- Host
- Port
- Username
- Password
- Database Name

---

## DAG Workflow

The DAG performs the following tasks.

1. Detect a new CSV file
2. Generate Batch ID
3. Store data in Raw Layer
4. Transform Raw → Bronze
5. Load Bronze into MySQL
6. Transform Bronze → Silver
7. Load Silver into MySQL
8. Generate Gold Sales Summary
9. Load Gold into MySQL
10. Display Pipeline Summary

---

## Triggering the Pipeline

Place a CSV file inside

```
External_CSVs/incoming/
```

Then trigger the DAG from the Airflow UI.

The pipeline processes one CSV file per execution.

After successful execution, the processed file is moved to

```
External_CSVs/processed/
```

---

## Expected Output

Successful execution creates:

- Raw CSV
- Bronze CSV
- Silver CSV
- Gold CSV

and loads data into

- orders
- orders_silver
- sales_summary

Refer to the screenshots in the images folder for DAG execution and Graph View.