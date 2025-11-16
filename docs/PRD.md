# Product Requirements Document (PRD)

**Document Status:** Draft
**Version:** 1.0
**Author:** Hanish Paturi
**Date:** 2025-11-16

## 1. Product Overview

The BoardGame Recommender System is a service that provides personalized board game recommendations via a REST API. It leverages a hybrid machine learning model combining content-based and collaborative filtering techniques to deliver relevant suggestions tailored to individual user tastes and contextual needs.

## 2. Goals & Objectives

* **Product Goal:** To provide users with accurate, personalized, and context-aware board game recommendations.
* **Business Goal:** To serve as a production-quality portfolio project that showcases advanced MLOps and software engineering skills.
* **Success Metrics:**
  * Offline evaluation metrics (Precision@10, NDCG@10) for the hybrid model should outperform individual models.
  * API latency (p95) should remain under 500ms.
  * The system must be deployable and maintainable at zero cost.

## 3. Functional Requirements

| ID | Requirement | Details | Priority |
| :--- | :--- | :--- | :--- |
| **FR-1** | **Content-Based Recommendations** | The system must provide recommendations for a given game based on the similarity of its metadata (description, mechanics, categories). | Must-Have |
| **FR-2** | **Collaborative Filtering** | The system must provide personalized recommendations for a given user based on their historical rating data and the behavior of similar users. | Must-Have |
| **FR-3** | **Hybrid Recommendation Model** | The system must be able to blend the scores from the RAG and CF models to produce a single, ranked list of recommendations. | Must-Have |
| **FR-4** | **Contextual Filtering** | API endpoints must support filtering of recommendation results based on parameters like `player_count`, `max_play_time`, and `complexity`. | Should-Have |
| **FR-5** | **API Service** | All recommendation logic must be exposed via a REST API with clear, documented endpoints for each function. | Must-Have |
| **FR-6** | **Data Update Pipeline** | The system must include an automated, periodic (e.g., weekly/monthly) pipeline to refresh game and rating data from the BGG API. | Should-Have |

## 4. Non-Functional Requirements

| ID | Requirement | Acceptance Criteria |
| :--- | :--- | :--- |
| **NFR-1** | **Performance** | 95th percentile API response time for recommendation endpoints must be less than 500 milliseconds under a load of 100 concurrent users. |
| **NFR-2** | **Scalability** | The architecture must be stateless and containerized (Docker) to allow for horizontal scaling of the API service. |
| **NFR-3** | **Cost** | All technologies and infrastructure must fall within the free-tier limits of their respective providers (e.g., Snowflake, Railway/Render). |
| **NFR-4** | **Maintainability** | The project must include a CI/CD pipeline that automates testing, linting, and deployment on every push to the main branch. |
| **NFR-5** | **Security** | The system will not store any user PII. All secrets (API keys, database credentials) must be managed via environment variables, not in source code. |
| **NFR-6** | **Documentation** | The API must have auto-generated, interactive documentation (via FastAPI/OpenAPI). HLD and LLD documents must be maintained. |

## 5. Use Cases & User Flow

* **Use Case 1: Cold Start User (Content-Based)**
    1. User provides one or more game IDs they like (e.g., `[174430]`).
    2. The system calls the RAG model to find games with the most similar text embeddings.
    3. The system returns a ranked list of 10 similar games.

* **Use Case 2: Experienced User (Collaborative Filtering)**
    1. User provides their unique user ID.
    2. The system calls the Collaborative Filtering model.
    3. The model predicts ratings for games the user has not yet played based on their taste profile.
    4. The system returns a ranked list of the 10 games with the highest predicted ratings.

## 6. Assumptions & Dependencies

* **Assumption:** The Kaggle dataset is a representative and sufficient starting point for bootstrapping the models.
* **Assumption:** The BGG API will remain available and its terms of use will continue to permit this non-commercial project.
* **Dependency:** The system relies on the availability of the free tiers from Snowflake and a cloud hosting provider. A change in their terms could impact the project.
* **Dependency:** The `sentence-transformers` and `implicit` Python libraries are core to the modeling approach.

## 7. Out of Scope (For MVP)

* **User Authentication:** The initial version will identify users by a simple ID string; a full authentication/authorization system is out of scope.
* **Frontend UI:** This PRD covers the backend service and API only. The development of a client-side user interface is a separate project.
* **A/B Testing Framework:** An online testing framework to compare different models with live traffic is out of scope for the MVP.
* **Real-time "Online" Learning:** The models will be retrained on a batch schedule. Real-time updates to the model based on every new user interaction are out of scope.
