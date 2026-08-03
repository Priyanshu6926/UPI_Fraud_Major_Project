# UPI Fraud Detection — Hybrid Anomaly Detection System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-111111?style=for-the-badge)](https://xgboost.readthedocs.io/)

An end-to-end, batch-processing research pipeline designed to detect anomalous and fraudulent Unified Payments Interface (UPI) transactions using a hybrid modeling approach (Supervised Classification + Unsupervised Anomaly Detection).

---

## 📌 Project Overview

Digital payment systems like UPI process millions of transactions daily, making rapid and accurate fraud identification critical. This project implements a batch machine learning framework that:
1. Ingests diverse transaction datasets from multiple sources.
2. Standardizes disparate raw records into a unified **Common Schema**.
3. Performs domain-specific feature engineering (transaction velocity, frequency, account delta).
4. Trains **Supervised Classification Models** (XGBoost & Random Forest) to classify known fraud vectors.
5. Trains **Unsupervised Anomaly Detection Models** (Isolation Forest & Local Outlier Factor) to flag zero-day suspicious behavior patterns.
6. Offers dual local testing dashboards:
   - **Streamlit App**: Lightweight Python testing UI.
   - **Vite React + FastAPI**: Modern full-stack interactive dashboard.

---

## ⚙️ System Architecture

```text
               +----------------------------------+
               |           Raw Datasets           |
               | (PaySim, UPI 2024, IEEE, Zenodo) |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               |      Schema Mapping Module       |
               |     (Standardized Schema)        |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               | Feature Engineering & Preprocessing|
               +----------------------------------+
                                |
                +---------------+---------------+
                |                               |
                v                               v
   +-------------------------+     +-------------------------+
   |    Supervised Models    |     |   Unsupervised Models   |
   | (XGBoost / Random Forest)|     |  (Isolation Forest/LOF) |
   +-------------------------+     +-------------------------+
                |                               |
                +---------------+---------------+
                                |
                                v
               +----------------------------------+
               |    Model Evaluation & Reports    |
               +----------------------------------+
                                |
       +------------------------+------------------------+
       |                                                 |
       v                                                 v
+-----------------------------+               +-----------------------------+
|    Streamlit Dashboard UI   |               |   FastAPI + React Frontend  |
+-----------------------------+               +-----------------------------+
```

---

## 📁 Repository Structure

```text
UPI-Fraud-Detection/
├── api/                      # FastAPI service for React frontend model inference
│   ├── __init__.py
│   └── main.py
├── app/                      # Streamlit testing dashboard & prediction engine
│   ├── components/
│   ├── app.py
│   ├── dashboard.py
│   └── prediction_engine.py
├── data/                     # Dataset storage (Git-ignored CSVs/Parquet)
│   ├── raw/                  # Place original downloaded datasets here
│   ├── processed/            # Preprocessed datasets & feature matrices
│   └── merged/               # Unified schema output dataset
├── frontend/                 # Vite + React frontend dashboard
│   ├── src/
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── models/                   # Saved model artifacts (.pkl files)
├── notebooks/                # Exploratory Jupyter Notebooks
│   ├── eda.ipynb
│   ├── preprocessing.ipynb
│   ├── feature_engineering.ipynb
│   ├── supervised_model.ipynb
│   └── anomaly_detection.ipynb
├── reports/                  # Generated evaluation plots & JSON metrics
├── src/                      # Core python pipeline modules
│   ├── data_loader.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── sampling.py
│   ├── schema_mapping.py
│   ├── supervised_model.py
│   ├── anomaly_detection.py
│   └── utils.py
├── .gitignore
├── main.py                   # Main pipeline entry point
├── README.md
├── RUN_COMMANDS.md           # Execution reference guide
└── requirements.txt          # Python dependencies
```

---

## 📊 Standardized Common Schema

All incoming raw datasets are transformed into the following common schema:

| Feature Name | Description |
| :--- | :--- |
| `transaction_id` | Unique transaction identifier |
| `timestamp` | Date & time of the transaction |
| `amount` | Transaction monetary value |
| `sender_id` | Account ID initiating the payment |
| `receiver_id` | Beneficiary Account ID |
| `device_type` | Device category used (Mobile, Web, POS) |
| `merchant_category` | Category of recipient merchant |
| `location` | Geographic origin of transaction |
| `transaction_type` | Type (TRANSFER, PAYMENT, CASH_OUT, etc.) |
| `fraud_label` | Target binary label (1 = Fraud, 0 = Legitimate) |

---

## 📂 Datasets Required

To run the complete batch pipeline, download the following public datasets and place the `.csv` files into the `data/raw/` folder:

1. **PaySim Dataset** (Kaggle)
2. **UPI Transaction 2024** (Kaggle)
3. **IEEE Fraud Detection** (Kaggle)
4. **Digital Payment Transactions** (Zenodo)

---

## 🚀 Quickstart Guide

### 1. Environment Setup

Clone the repository and create a Python virtual environment:

```bash
git clone https://github.com/Priyanshu6926/UPI_Fraud_Major_Project.git
cd UPI_Fraud_Major_Project

# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Run the Data & Model Pipeline

Executes schema mapping, feature engineering, model training, and generates report metrics:

```bash
python main.py --all
```

---

### 3. Launching the Testing Dashboards

#### Option A: Streamlit Dashboard (Python UI)

```bash
streamlit run app/app.py
```

#### Option B: Vite React Dashboard + FastAPI Backend

**Terminal 1 — Backend API:**
```bash
uvicorn api.main:app --reload
```

**Terminal 2 — Frontend UI:**
```bash
cd frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🛡️ Scope & Boundaries

- **Focus**: Research, dataset mapping, feature extraction, supervised ML evaluation, and unsupervised anomaly detection.
- **Out of Scope**: Production payment gateway integration, real-time banking stream ingestion, live authentication, or automated transaction blocking.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
