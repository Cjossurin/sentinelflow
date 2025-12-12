# 🛡️ SentinelFlow: Network Anomaly Detection System

**SentinelFlow** is a production-ready machine learning pipeline built
to detect network intrusions in real time. It identifies **Brute
Force**, **DoS/DDoS**, and **Web Attacks** with **99.9% accuracy**.

## 🚀 Features

-   **Multi-Vector Threat Detection**\
    Detects 7+ attack types including FTP/SSH Patator, DoS
    Hulk/GoldenEye, SQL Injection, and XSS.

-   **Production API**\
    Real-time REST API built with **FastAPI**.

-   **Containerized Deployment**\
    Fully Dockerized for seamless "write once, run anywhere" execution.

-   **Robust Preprocessing Pipeline**\
    Automatically handles infinite values, missing data, and feature
    scaling.

## 🛠️ Tech Stack

-   **Core:** Python 3.11, Pandas, NumPy\
-   **ML:** Scikit-Learn (Random Forest Classifier)\
-   **API:** FastAPI, Uvicorn\
-   **Ops:** Docker, Git

## 📊 Model Performance

Model v3 was trained on the **CICIDS2017** dataset (1.3M records) and
achieved:

-   **Accuracy:** 99.92%\
-   **Detection Rate:** 99.8% (known attacks)\
-   **False Alarm Rate:** \< 0.04%

## ⚡ Quick Start (Docker)

### 1. Build the Container

``` bash
docker build -t sentinelflow-api -f docker/Dockerfile .
```

### 2. Run the API

``` bash
docker run -d -p 8005:8000 --name sentinel-api sentinelflow-api
```

### 3. Test the Endpoint

The API listens at:

    http://localhost:8005

Send a `POST` request to `/predict` with a list of **78 network
features**.

## 📂 Project Structure

    src/api/        # FastAPI application code
    notebooks/      # Jupyter notebooks for analysis & training
    models/         # Serialized ML models and scalers (.pkl)
    docker/         # Container configuration
