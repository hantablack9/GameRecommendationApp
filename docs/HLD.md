# High-Level Design (HLD): BoardGame Recommender System

**Document Status:** Draft
**Version:** 1.0
**Author:** Hanish Paturi
**Date:** 2025-11-16

## 1. Context & Objective

This document outlines the high-level architecture for the BoardGame Recommender System. The objective is to design a scalable, maintainable, and low-cost MLOps platform capable of ingesting data, training multiple recommendation models, and serving predictions via a REST API. This system serves as a portfolio project demonstrating end-to-end ML engineering capabilities.

## 2. Design Overview & Architecture

The system follows a modern ELT (Extract, Load, Transform) architecture combined with a batch training and online inference pattern. It is composed of five major subsystems: Data Ingestion, Data Warehouse & Transformation, Model Training, Model Serving, and Monitoring/Logging.

### 2.1. Architecture Diagram

```plaintext
┌──────────────────┐   1. Load  ┌──────────────────┐   2. Transform  ┌─────────────────────┐
│   Raw CSV Data   ├───────────►│ Snowflake (RAW)  ├────────────────►│Snowflake (ANALYTICS)│
│   (.csv.gz)      │ (Python)   │     Schema       │      (dbt)      │      Schema         │
└──────────────────┘            └──────────────────┘                 └─────────┬───────────┘
                                                                               │ 3. Generate ML Artifacts
                                                                               │ (Python Training Script)
                                                                               ▼
                                                                     ┌───────────────────┐
                                                                     │  Model Artifacts  │
                                                                     │ - cf_model.pkl    │
                                                                     │ - rag_index.faiss │
                                                                     └─────────┬─────────┘
                                                                               │ 4. Load for Serving
                                                                               │
                                                                               ▼
                                                                     ┌───────────────────┐
                                                                     │   FastAPI Server  │
                                                                     │  (for inference)  │
                                                                     └───────────────────┘
```

## 3. Component Design

1.  **Data Ingestion (`src/recsys/scripts/`)**:
    *   A set of Python scripts responsible for the "E" (Extract) and "L" (Load) of the ELT process.
    *   `setup_snowflake_db.py`: An idempotent script to create the database, schemas (`RAW_DATA`, `ANALYTICS`), tables, and stages in Snowflake.
    *   A future `load_raw_data.py` script will handle uploading local CSV data to the Snowflake stage and using `COPY INTO` to load it into the `RAW_DATA` tables.

2.  **Data Warehouse & Transformation (`dbt_project/`)**:
    *   **Technology**: Snowflake (Storage/Compute), dbt (Transformation).
    *   **RAW_DATA Schema**: Contains raw, untouched data loaded directly from source files.
    *   **ANALYTICS Schema**: Contains cleaned, transformed, and feature-engineered tables built by dbt. This is the single source of truth for all downstream applications.
    *   **dbt Models**: A Directed Acyclic Graph (DAG) of SQL `SELECT` statements that build staging models (basic cleaning), intermediate models (joins), and final data marts (e.g., `mart_games_with_features`) ready for ML.

3.  **Model Training (`src/recsys/models/trainer.py`)**:
    *   A Python script that runs *after* the dbt pipeline.
    *   It connects to the `ANALYTICS` schema in Snowflake to fetch the clean training data.
    *   It orchestrates the training of the Collaborative Filtering model and the generation of the RAG artifacts (FAISS index, metadata).
    *   The trained artifacts are versioned and stored in the `/models` directory.

4.  **Model Serving (`src/recsys/api/`)**:
    *   **Technology**: FastAPI.
    *   A RESTful API server that loads the trained model artifacts from the `/models` directory into memory on startup.
    *   It exposes endpoints (e.g., `/recommend/hybrid`) that accept user input, perform inference using the loaded models, and return JSON responses.
    *   Containerized with Docker for consistent deployment.

## 4. Technology Stack Justification

*   **Snowflake**: Chosen for its separation of storage and compute, industry relevance, and available free tier, making it ideal for a cost-effective yet powerful data warehouse.
*   **dbt**: Chosen as the industry standard for data transformation. It enforces modularity, provides automated testing and documentation, and allows for building reliable, maintainable data pipelines using only SQL.
*   **FAISS**: Chosen for its high-speed, in-memory vector search capabilities. It provides state-of-the-art performance at zero cost and is sufficient for the project's scale (under 1 million vectors).
*   **FastAPI**: Chosen for its high performance, native `async` support, and automatic generation of interactive OpenAPI documentation, which drastically speeds up API development and testing.

## 5. Quality Attributes

*   **Scalability**: The serving layer (FastAPI) is stateless and can be scaled horizontally by running more Docker containers. The data layer (Snowflake) can be scaled up by resizing the virtual warehouse with a single command.
*   **Reliability**: The use of dbt tests ensures data quality and integrity in the `ANALYTICS` layer. The API will have health check endpoints for monitoring. The ELT architecture decouples the analytical data from the raw data, preventing corruption.
*   **Security**: No PII is stored. All credentials and secrets are managed via environment variables (e.g., using `.env` file or platform secrets), not checked into source control.
*   **Cost**: The entire stack is designed to operate within the free-tier limits of services like Snowflake and cloud hosting platforms (e.g., Railway).

---
