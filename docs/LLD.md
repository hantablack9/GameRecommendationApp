# Low-Level Design (LLD): Model Training Pipeline

**Document Status:** Draft
**Version:** 1.0
**Author:** Hanish Paturi
**Date:** 2025-11-16

## 1. Introduction & Scope

This document provides a detailed design for the model training pipeline, orchestrated by a `trainer.py` module. Its scope is to define the classes, data structures, and algorithms required to fetch clean data from Snowflake and produce all necessary model artifacts for serving.

## 2. Class & Module Design

The training process will be encapsulated within a `Trainer` class, which utilizes the model classes defined in `src/recsys/models/`.

```
+---------------------------+
|      Trainer              |
+---------------------------+
| - snowflake_creds: dict   |
| - models_output_dir: Path |
+---------------------------+
| + __init__()              |
| + _fetch_data(query): df  |
| + train_rag_model()       |
| + train_cf_model()        |
| + run_pipeline()          |
+---------------------------+
         |
         | uses
         ▼
+---------------------------+      +---------------------------+
|    RAGRecommender         |      |    CollaborativeFilter    |
+---------------------------+      +---------------------------+
| - embedding_model         |      | - als_model               |
| - faiss_index             |      +---------------------------+
+---------------------------+      | + fit(ratings_df)         |
| + fit(games_df)           |      | + save(path)              |
| + save(path)              |      | + load(path)              |
+---------------------------+      +---------------------------+
```

## 3. Data Structures and Algorithms

### 3.1. RAG Model Training (`train_rag_model`)

1.  **Algorithm**:
    1.  Invoke `_fetch_data` with SQL query: `SELECT GAME_ID, NAME, DESCRIPTION, CATEGORIES, MECHANICS FROM ANALYTICS.MART_GAMES`.
    2.  **Feature Concatenation**: Create a new column `embedding_text` by concatenating text from `NAME`, `DESCRIPTION`, `CATEGORIES`, and `MECHANICS` with descriptive prefixes (e.g., "Name: ...; Description: ...").
    3.  **Embedding Generation**: Load the `all-MiniLM-L6-v2` model using `sentence-transformers`. Call `model.encode()` on the `embedding_text` column to generate a NumPy array of vectors.
    4.  **FAISS Indexing**:
        *   Initialize a `faiss.IndexFlatL2` with the dimension of the embeddings (384).
        *   Add the generated embeddings to the index using `index.add()`.
    5.  **Artifact Serialization**:
        *   Save the FAISS index to `models/v1/rag_index.faiss` using `faiss.write_index()`.
        *   Create a metadata dictionary `{'ids': [game_id_1, game_id_2, ...]}` preserving the order of the input DataFrame.
        *   Save the metadata as a JSON file to `models/v1/metadata.json`.

2.  **Data Structures**:
    *   **Input**: pandas DataFrame from Snowflake.
    *   **Intermediate**: NumPy array of `float32` embeddings.
    *   **Output**: `rag_index.faiss` (binary), `metadata.json` (JSON).

### 3.2. Collaborative Filtering Model Training (`train_cf_model`)

1.  **Algorithm**:
    1.  Invoke `_fetch_data` with SQL query: `SELECT USER_ID, GAME_ID, RATING FROM ANALYTICS.MART_USER_RATINGS`.
    2.  **Matrix Creation**:
        *   Convert `USER_ID` and `GAME_ID` to categorical codes (integer indices) to ensure a dense mapping.
        *   Create a `scipy.sparse.csr_matrix` with users as rows, items as columns, and ratings as data.
    3.  **Model Training**:
        *   Instantiate the `implicit.als.AlternatingLeastSquares` model with configured factors and regularization.
        *   Call `model.fit()` on the sparse matrix.
    4.  **Artifact Serialization**:
        *   Save the trained ALS model object to `models/v1/cf_model.pkl` using `pickle` or `joblib`.
        *   Save the user and item mapping (e.g., `{'user_id_to_idx': {...}}`) to a separate JSON file for inference lookup.

2.  **Data Structures**:
    *   **Input**: pandas DataFrame of user-item-rating triplets.
    *   **Intermediate**: `scipy.sparse.csr_matrix`.
    *   **Output**: `cf_model.pkl` (binary pickle file), `cf_mappings.json` (JSON).

## 4. Error Handling

The pipeline is designed to **fail fast**.

*   **Database Connection**: The `_fetch_data` method will be wrapped in a `try...except` block. On `snowflake.connector.Error`, it will log the error and raise a `ConnectionError`, causing the pipeline to terminate immediately.
*   **File I/O**: All file writing operations (`faiss.write_index`, `json.dump`, `pickle.dump`) will be in `try...except` blocks. On `IOError` or `PermissionError`, the error will be logged, and the application will exit with a non-zero status code to signal failure to CI/CD systems.
*   **Data Validation**: A check will be performed after fetching data to ensure the DataFrame is not empty. If it is, a `ValueError` will be raised, causing the pipeline to fail with a clear message.

## 5. Security Considerations

*   The `trainer.py` script will access Snowflake credentials exclusively through environment variables (`os.getenv`). No credentials will be hardcoded.
*   The script should operate using a dedicated ML user role in Snowflake with read-only access to the `ANALYTICS` schema, preventing any accidental modification of the source of truth.

---
