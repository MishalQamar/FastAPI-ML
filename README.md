# FastAPI-ML

This project is a small end‑to‑end example of deploying a machine learning model as a production‑style API using FastAPI.
It covers the full flow from data and training code, to a packaged model artifact, to an HTTP prediction service that can be containerized and monitored.

## What this project demonstrates
- **Serving ML models with FastAPI**: the `app.main` module exposes REST endpoints for health checks, authentication, and model predictions.
- **Separation of concerns**: prediction logic lives in `app/services/model_service.py`, configuration and dependencies in `app/core`, and HTTP routing in `app/api`.
- **Model lifecycle**: the trained model is stored as a serialized artifact in `app/models/model.joblib`, and the `training/` package contains the scripts and utilities used to train it from raw data.
- **Data‑driven example**: the `data/car-details.csv` file is an example dataset used by the training code to build the model.
- **Production readiness**: Docker and Render configuration files (`Dockerfile`, `render.yaml`, `prometheus.yml`) illustrate how the service can be containerized, deployed, and monitored.

## Tech stack
- **FastAPI** for the web framework and automatic OpenAPI documentation.
- **Python** for the API, training scripts, and model code.
- **Joblib** (via scikit‑learn ecosystem) for serializing the trained model.
- **Docker + Render** for containerization and deployment.
- **Prometheus** for metrics scraping configuration.
