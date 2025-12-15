
📈 Dhaka Finance Navigator: Stock Prediction API
Project Status
Item	Status
API Endpoint	Will be populated after successful Render deployment.
Model	Random Forest Regressor
Deployment	Render (Dockerized Web Service)
Source Folder	APP_TEST (Local folder)
📋 Overview

The Dhaka Finance Navigator project provides a resilient and containerized RESTful API for predicting stock prices. The service is built with Flask and deployed via Docker on Render's Free Tier, ensuring high availability and cost-efficiency for basic use.

This API serves a trained Random Forest Regressor model that processes engineered features (e.g., lagged prices, technical indicators) and returns a predicted stock price, allowing for seamless integration into dashboards, mobile applications, or trading tools.
🌟 Key Features

    RESTful API: Predicts stock prices via the standardized /predict endpoint, accepting JSON input and returning JSON output.

    Containerized Deployment: Uses a Dockerfile for environment consistency and quick deployment on any Docker-compatible platform (currently Render).

    Machine Learning: Utilizes a Random Forest Regressor model, saved as random_forest_model.pkl.

    Data Consistency: Feature names and processing are managed by the saved model_features.pkl file.

🛠️ Technology Stack
Component	Technology	Purpose
Web Framework	Flask	Lightweight Python server for API routing.
Production Server	gunicorn	WSGI HTTP server used within the Docker container.
Machine Learning	scikit-learn (Random Forest)	Core prediction logic.
Data Handling	pandas, numpy	Data manipulation and feature preparation.
Deployment	Docker, Render	Containerization and free hosting platform.
🚀 Setup and Deployment
1. Local Setup

To run and test the API locally, you need Python 3.x and the required dependencies.
Bash

# Clone the repository
git clone https://github.com/sifatbhuiyan0909/Dhaka-Finance-Navigator.git
cd Dhaka-Finance-Navigator

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application using the development server
python app.py

(The API will run locally at: http://127.0.0.1:5000/)
2. Deployment on Render (Via Docker)

This project is configured for automated deployment on Render directly from this GitHub repository.

The configuration relies on the following files in the repository root:

    Dockerfile (Specifies the environment and runs gunicorn app:app).

    requirements.txt (Includes gunicorn and ML libraries).

The service runs the Flask application (app.py) on port 8080. Render automatically detects the Dockerfile, builds the container, and serves the application.
💡 API Usage

The main endpoint for making predictions is /predict.
Method	URL	Description
POST	/predict	Returns the predicted stock price based on input features.
Example Request

The API expects a JSON payload containing the exact features the model was trained on.
Bash

curl -X POST \
  https://YOUR-RENDER-URL.onrender.com/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "lag_1": 150.25,
    "volume_ma_5": 8500000,
    "rsi_14": 55.3,
    "macd": 0.5
  }'

Example Response (Success)
JSON

{
  "prediction": 150.98,
  "status": "success"
}

🤝 Contributing

We welcome contributions! Please open an issue or submit a pull request if you have suggestions for new features, better model performance, or bug fixes.

Disclaimer: This stock prediction model is for educational and experimental purposes only. It is not financial advice. Trading involves risk. 
** well i am just beginning and it was created after so many errors and trails and i expect that there are mistakes i missed. so open to be helped **
