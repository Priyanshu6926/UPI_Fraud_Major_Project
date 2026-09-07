# Deployment & Hosting Guide for Resume

This project is configured as a **single-container, full-stack application**:
- The **FastAPI backend** serves the ML prediction API and pre-calculated research analytics.
- The **React frontend** is built into static assets and served directly at `/` from the same domain.
- **Production Models Included**: The production XGBoost model, Isolation Forest, preprocessors, and context files (~4.9 MB total) are committed to the repository and ready for immediate serving.

---

## Option 1: Free Hosting on Render.com (Recommended)

Render offers a free tier that connects directly to your GitHub repository and automatically deploys whenever you push changes.

### Step-by-Step Instructions:
1. **Sign Up / Log In**:
   - Go to [render.com](https://render.com) and click **Sign in with GitHub**.
2. **Create a New Web Service**:
   - In your Render Dashboard, click the **New +** button in the top right.
   - Select **Web Service**.
3. **Connect Your GitHub Repository**:
   - Select **Build and deploy from a Git repository**.
   - Connect and choose your repository: `Priyanshu6926/UPI_Fraud_Major_Project`.
4. **Configure Service Details**:
   - **Name**: `upi-fraud-detection` (or any custom name)
   - **Region**: Choose the closest region (e.g. `Oregon (US West)` or `Singapore`)
   - **Runtime**: **Docker** (Render will automatically detect the `Dockerfile`)
   - **Instance Type**: **Free**
5. **Deploy**:
   - Click **Create Web Service**.
   - Render will automatically build the React frontend, install Python dependencies, load the ML models, and start the service.
   - Once deployment completes (usually 2–3 minutes), you will get your live URL:
     ```text
     https://upi-fraud-detection.onrender.com
     ```

---

## Option 2: Free Hosting on Hugging Face Spaces

Hugging Face Spaces is popular in the AI/ML industry and looks great on developer resumes.

### Step-by-Step Instructions:
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and log in.
2. Click **Create new Space**.
3. Set **Space Name**: `upi-fraud-detection`.
4. Choose **Space SDK**: **Docker** -> **Blank**.
5. Set Visibility: **Public**.
6. Follow instructions to push this repository code to your Space Git remote, or connect your GitHub repository directly.

---

## Resume Showcase Bullet Points

You can format your project on your resume like this:

> **UPI Fraud & Anomaly Detection System** | *Python, FastAPI, React, XGBoost, Scikit-Learn, Docker*
> - **Live Demo**: `https://upi-fraud-detection.onrender.com` | **GitHub**: `https://github.com/Priyanshu6926/UPI_Fraud_Major_Project`
> - Engineered an end-to-end dual-signal fraud detection system processing high-velocity UPI transactions using supervised XGBoost and unsupervised Isolation Forest models.
> - Implemented weighted dual-signal fusion calibration to resolve ambiguous transactions with explainable post-transaction risk diagnostics.
> - Built a full-stack dashboard in React & FastAPI, containerized via multi-stage Docker builds, and deployed for interactive real-time simulation.
