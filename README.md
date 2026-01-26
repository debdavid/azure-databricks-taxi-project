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

## 📸 Architecture & Execution
  
<img width="909" height="271" alt="Screenshot 2026-01-26 at 12 57 36 pm" src="https://github.com/user-attachments/assets/bf2dde4d-3fd0-4326-923c-14c8bdf4f960" />

Figure 1: Successful ingestion of NYC Taxi data into Azure Blob Storage.

---

## 📂 Repository Structure
* `/notebooks` - PySpark notebooks for ingestion and transformation.
  
