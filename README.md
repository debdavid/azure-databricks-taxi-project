# 🚖 NYC Taxi Data Lakehouse (Azure + Databricks)

## 🎯 Project Goal
Building an end-to-end Data Engineering pipeline to analyse NYC Taxi data. The goal is to move from raw CSV data to actionable insights using the "Medallion Architecture" (Bronze/Silver/Gold).

---

## 🏗️ Tech Stack
* **Cloud:** Microsoft Azure
* **Compute:** Azure Databricks (Spark 3.5, Scala 2.12)
* **Storage:** Azure Data Lake Gen2 (Standard Blob WASBS)
* **Orchestration:** Azure Data Factory (Planned)
* **Language:** Python (PySpark)

---

## 📅 Progress Log
* **Phase 1: Infrastructure Setup** (Completed Jan 25)
    * Provisioned Azure Resource Group and Storage Account.
    * Deployed Azure Databricks Workspace (Standard Tier).
    * Configured Spark Cluster (Single Node) for cost optimisation.
    * Established secure connection between Databricks and Blob Storage via WASBS protocol.

---

## 🏗️ ELT Pipeline Architecture
The pipeline follows the **Medallion Architecture** (Bronze → Silver → Gold) to ensure data quality and traceability.

### 🥉 Phase 1: Bronze Layer (Ingestion)
**Goal:** Ingest raw historical data from external public sources into the internal Data Lake without modification.
* **Source:** NYC Taxi & Limousine Commission (TLC) Trip Record Data.
* **Method:** Programmatic extraction using Python (`requests`) to fetch monthly Parquet archives.
* **Storage:** Azure Blob Storage (Container: `raw`), utilising the **WASBS** protocol for Spark connectivity.

**Execution Evidence:**

<img width="909" height="271" alt="Screenshot 2026-01-26 at 12 57 36 pm" src="https://github.com/user-attachments/assets/bf2dde4d-3fd0-4326-923c-14c8bdf4f960" />

*Figure 1: Successful ingestion of NYC Taxi data into Azure Blob Storage.*

---

### 🥈 Phase 2: Silver Layer (Transformation & Cleaning)
**Goal:** Cleanse and validate data to ensure it is trusted for downstream analysis.
* **Schema Enforcement:** Renamed columns from legacy formats (e.g., `tpep_pickup_datetime`) to business-standard naming conventions.
* **Data Quality Filters:**
    * Removed trips with **0 passengers** (Data Entry Errors).
    * Removed trips with **negative fares** (Refunds/Disputes).
* **Storage Format:** Saved as **Delta Tables** (Delta Lake) to enable **ACID transactions** and scalable metadata handling.

**Data Quality Impact:**

<img width="913" height="453" alt="Screenshot 2026-01-26 at 1 32 27 pm" src="https://github.com/user-attachments/assets/975bad72-0413-425c-8a81-85401625c621" />

*Figure 2: Removed approximately ~200,000 invalid records (~7% of source data) to improve analytical accuracy.*


---

## 📂 Repository Structure
* `/notebooks` - PySpark notebooks for ingestion and transformation.
  
