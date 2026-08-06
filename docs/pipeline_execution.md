# Pipeline Execution Guide

## Step 1

Start Apache Airflow.

---

## Step 2

Copy a retail CSV file into

```
External_CSVs/incoming/
```

---

## Step 3

Trigger the DAG

```
retail_data_pipeline
```

from the Airflow UI.

---

## Step 4

Monitor the DAG execution.

The pipeline performs

- Data Ingestion
- Validation
- Cleaning
- Duplicate Removal
- Business Rule Processing
- MySQL Loading
- Sales Summary Generation

---

## Step 5

Verify the Graph View.

Expected status

- All tasks successful
- No failed tasks

Screenshot

```
images/airflow_graph.png
```

---

## Step 6

Verify successful DAG execution.

Screenshot

```
images/airflow_success.png
```

---

## Pipeline Summary

Each successful execution

- Processes one CSV file
- Generates a unique Batch ID
- Stores Bronze data in MySQL
- Stores Silver data in MySQL
- Generates Gold sales metrics
- Loads the sales summary into MySQL
- Moves the processed file to the processed folder

The pipeline can be executed repeatedly by placing a new CSV file into the incoming folder.