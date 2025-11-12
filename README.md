# Game Recommendation System

This repository contains a Python script for a Game Recommendation System built using Streamlit. The recommendation system utilizes K-Means clustering and cosine similarity to suggest games based on various features such as categories, themes, popularity, and more.

### Description
The script app.py implements a Game Recommendation System that allows users to input their preferred games and receive recommendations based on similar games. The recommendation is generated using K-Means clustering and cosine similarity metrics.

### Features
**Game Selection:** Users can select up to three games from a dropdown menu.

**Recommendation Generation:** Upon selecting games, users can generate recommendations based on similarities in categories, themes, popularity, and more.

**Interactive UI:** The user interface provides an intuitive experience, allowing users to interact with the system effortlessly.

**Image Display:** Game recommendations are accompanied by images fetched from online sources.

### File Structure

```plaintext
boardgame-recommender/
├── README.md
├── pyproject.toml              # Modern Python packaging
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── .gitignore
├── docker-compose.yml
├── Dockerfile
│
├── notebooks/                 # POC & Exploration
│   ├── 01_eda.ipynb
│   ├── 02_model_experiments.ipynb
│   └── streamlit_poc.py       # Original POC
│
├── data/                      # Data directory (gitignored except README)
│   ├── raw/                   # Kaggle dataset for POC goes here
│   │   ├── games.csv
│   │   ├── user_ratings.csv
│   │   └── ...
│   ├── processed/             # Cleaned/transformed data
│   └── embeddings/            # Stored embeddings
│
├── models/                    # Trained model artifacts
│   └── v1/
│       ├── rag_index.faiss
│       ├── cf_model.pkl
│       └── metadata.json
│
├── src/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py        # Pydantic settings
│   │   └── logging_config.py
│   │
│   ├── data/                  # Data processing layer
│   │   ├── __init__.py
│   │   ├── loader.py          # Load Kaggle datasets
│   │   ├── preprocessor.py   # Clean & transform
│   │   └── feature_engineering.py
│   │
│   ├── models/                # ML models
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract base classes
│   │   ├── rag_recommender.py     # Content-based (embeddings)
│   │   ├── collaborative_filter.py # CF implementation
│   │   ├── hybrid_recommender.py  # Combine RAG + CF
│   │   └── trainer.py        # Model training scripts
│   │
│   ├── api/                   # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   ├── dependencies.py   # Dependency injection
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── recommendations.py
│   │   │   ├── games.py
│   │   │   └── health.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── game.py
│   │       └── recommendation.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── distance_metrics.py   # # Computedistance_themes logic
│       ├── clustering.py         # KMeans clustering logic
│       └── cache.py             # Caching utilities
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_data/
│   ├── test_models/
│   │   ├── test_rag_recommender.py
│   │   ├── test_collaborative_filter.py
│   │   └── test_hybrid.py
│   └── test_api/
│       └── test_recommendations.py
│
├── scripts/                   # Utility scripts
│   ├── download_kaggle_data.py
│   ├── train_models.py
│   └── generate_embeddings.py
│
└── docs/
    ├── architecture.md
    ├── api_documentation.md
    └── model_design.md
```
**requirements.txt:** List of Python dependencies.

**README.md:** Documentation file providing information about the project.

## Acknowledgments
This project utilizes Streamlit for creating interactive web applications.
Data used for recommendation is sourced from external datasets (not included in this repository).

### Contributors

**Hanish Patturi** https://github.com/hantablack9
