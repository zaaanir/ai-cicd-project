# Automated CI/CD Pipeline for AI Application Deployment

This is a complete, production-ready project demonstrating an automated CI/CD pipeline for an AI-based web application (Fake News Detection). 

## Project Architecture

- **Backend (`/backend`)**: A Flask REST API that serves a Machine Learning model. The model is trained using scikit-learn (Naive Bayes with TF-IDF vectorization) to classify text as Real or Fake News.
- **Frontend (`/frontend`)**: A clean, modern, minimal UI built with HTML, CSS, and Vanilla JavaScript that interacts with the backend `/predict` endpoint.
- **CI/CD (`/.github/workflows`)**: A GitHub Actions workflow that automatically installs dependencies, trains the model, runs unit tests, and prepares for deployment upon any push to the `main` branch.

## Directory Structure

```
ai_cicd_project/
│
├── backend/                  # Flask API and ML Model
│   ├── model/
│   │   └── train_model.py    # Script to train and save the model (.pkl)
│   ├── tests/
│   │   └── test_app.py       # Unit tests for the API
│   ├── app.py                # Main Flask application
│   ├── Dockerfile            # Containerization instructions
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # User Interface
│   ├── index.html            # Main HTML file
│   ├── style.css             # Styling (Modern, Clean UI)
│   └── script.js             # API integration logic
│
├── .github/workflows/        # CI/CD Pipeline Configuration
│   └── ci-cd.yml             # GitHub Actions YAML file
│
└── README.md                 # Project Documentation
```

## Setup & Running Locally

### 1. Backend Setup

Open a terminal and navigate to the `backend` directory:
```bash
cd backend
```

Create and activate a virtual environment (optional but recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Train the ML model (This will generate the `fake_news_model.pkl` file):
```bash
python model/train_model.py
```

Run the Flask API:
```bash
python app.py
```
*The API will start running on http://127.0.0.1:5000*

### 2. Frontend Setup

Open another terminal and navigate to the `frontend` directory:
```bash
cd frontend
```

You can simply open `index.html` in your web browser, or use a local server like Live Server (VS Code extension) or Python's HTTP server:
```bash
python -m http.server 8000
```
*Open http://localhost:8000 in your browser.*

## Deployment Guide

### Backend Deployment (Render)
1. Push this code to a GitHub repository.
2. Go to [Render](https://render.com/) and create a new "Web Service".
3. Connect your GitHub repository.
4. Set the Root Directory to `backend`.
5. Environment: `Python 3`.
6. Build Command: `pip install -r requirements.txt && python model/train_model.py`
7. Start Command: `gunicorn app:app`
8. Click "Create Web Service". Render will now automatically deploy whenever you push to `main`.

### Frontend Deployment (Vercel)
1. Go to [Vercel](https://vercel.com/) and create a new Project.
2. Connect the same GitHub repository.
3. Edit the "Root Directory" to be `frontend`.
4. Leave build commands empty (since it's plain HTML/JS/CSS).
5. Click "Deploy". Vercel will now automatically deploy whenever you push to `main`.

**Important Update:** After deploying the backend, copy your Render URL (e.g., `https://my-app.onrender.com/predict`) and paste it into `frontend/script.js` on line 15 replacing the placeholder API_URL. Push this change to update the frontend.

## CI/CD Workflow Explanation

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml`.
- **Trigger**: It runs every time code is pushed to the `main` branch or a pull request is created.
- **Build & Test Job**:
  1. **Checkout**: Pulls the latest code.
  2. **Setup Python**: Installs Python 3.10.
  3. **Install Dependencies**: Installs the required Python packages for the backend.
  4. **Train Model**: Runs the training script to generate the model file needed for tests.
  5. **Run Tests**: Executes `pytest` to verify the `/predict` API endpoint works correctly.
- **Deploy Job**: If the tests pass, Render and Vercel (which are connected to the repo) automatically trigger their deployment processes (Continuous Deployment).

## Viva Preparation

**Q1: What is a CI/CD Pipeline?**
**Answer:** CI/CD stands for Continuous Integration and Continuous Deployment. It is an automated process where every code change is automatically built, tested (CI), and deployed to production (CD), reducing manual errors and speeding up delivery.

**Q2: What machine learning algorithm did you use and why?**
**Answer:** I used Multinomial Naive Bayes along with TF-IDF vectorization. TF-IDF converts text into numerical features, and Naive Bayes is a simple, lightweight, and effective algorithm for text classification tasks like spam or fake news detection.

**Q3: How does the Frontend communicate with the Backend?**
**Answer:** The frontend uses the JavaScript `fetch` API to send a POST request with the user's text in JSON format to the backend's `/predict` REST API endpoint. The backend processes it and returns the prediction in JSON format, which the frontend then displays.

**Q4: What is the purpose of Docker here?**
**Answer:** Docker packages the backend application and all its dependencies into a single container. This ensures that the application runs exactly the same way in any environment (development, staging, or production), solving the "it works on my machine" problem.

## Key Features
- **End-to-End Automation**: Fully automated testing and deployment.
- **RESTful API**: Standardized backend communication.
- **Machine Learning Integration**: Real-time inference through a web endpoint.
- **Modern UI**: Clean, responsive, and user-friendly interface.
- **Container-ready**: Dockerfile included for easy cloud deployment.
