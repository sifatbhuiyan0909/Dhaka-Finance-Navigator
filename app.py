import pandas as pd
import numpy as np
import pickle
from flask import Flask, request, jsonify 
import pandas_ta as ta
import os
import logging

# Set up logging to catch any errors during runtime
logging.basicConfig(level=logging.INFO)

# --- 1. Load Model and Features ---
MODEL_PATH = 'random_forest_model.pkl'
FEATURES_PATH = 'model_features.pkl'

try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(FEATURES_PATH, 'rb') as features_file:
        MODEL_FEATURE_NAMES = pickle.load(features_file)
    logging.info("Model and Feature List loaded successfully.")
    
except FileNotFoundError:
    logging.error(f"Deployment files not found. Check paths: {MODEL_PATH}, {FEATURES_PATH}")
    model = None
    MODEL_FEATURE_NAMES = []

# --- 2. Feature Engineering Logic (Mirrors Day 7 & 8) ---
def create_model_features(raw_data_df):
    """
    Transforms raw OHLCV data into the features the model expects (SMA, RSI, MACD, Lag_Return).
    The input DF must contain columns: Close, Open, High, Low, Volume.
    """
    df = raw_data_df.copy()
    
    # 1. Base Features (SMA) - Mirrors Day 7
    df['SMA_5'] = df['Close'].rolling(window=5, min_periods=1).mean()
    df['SMA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()

    # 2. Advanced Features (RSI, MACD, Lag_Return) - Mirrors Day 8
    df['RSI'] = ta.rsi(close=df['Close'], length=14)
    
    # MACD Calculation
    macd_result = ta.macd(close=df['Close'])
    if macd_result is not None and len(macd_result.columns) > 0:
        # Assumes MACD column is the first in the returned DF
        df['MACD'] = macd_result.iloc[:, 0]
    else:
        df['MACD'] = np.nan

    # Lagged Log Return
    df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Lag_Log_Return'] = df['Log_Return'].shift(1)
    
    # Drop rows where feature calculation resulted in NaN (usually the first few rows)
    df = df.dropna()
    
    # Select only the features the model was trained on (using the loaded list)
    # The order MUST match the order in MODEL_FEATURE_NAMES
    try:
        features_df = df[MODEL_FEATURE_NAMES]
    except KeyError as e:
        logging.error(f"Missing required feature columns: {e}")
        return None
        
    return features_df

# --- 3. Initialize Flask Application ---
app = Flask(__name__)

# --- 4. Define the Prediction Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500

    try:
        # 1. Get data sent via the POST request
        # The data is expected to be a list of daily dictionaries
        raw_data = request.get_json(force=True)
        raw_data_df = pd.DataFrame(raw_data)
        
        # Ensure raw data columns are correct (case-sensitive)
        required_cols = ['Close', 'Open', 'High', 'Low', 'Volume']
        if not all(col in raw_data_df.columns for col in required_cols):
             return jsonify({'error': f"Input data must contain: {required_cols}"}), 400

        # 2. Feature Engineering
        X_processed = create_model_features(raw_data_df)
        
        if X_processed is None or X_processed.empty:
            return jsonify({'prediction': 'No prediction (Not enough historical data provided to create features)'}), 200
        
        # We only predict on the most recent, fully processed row (the last row)
        X_final = X_processed.iloc[[-1]] 

        # 3. Model Prediction
        # Get the probability for both classes [P(Down), P(Up)]
        y_proba = model.predict_proba(X_final)[0]
        
        prediction = int(model.predict(X_final)[0])
        
        # 4. Format Output
        result = {
            'prediction': prediction, # 1 (Up) or 0 (Down)
            'confidence_up': round(y_proba[1], 4),
            'confidence_down': round(y_proba[0], 4),
            'model_info': 'Random Forest Classifier',
            'features_used': X_final.columns.tolist()
        }
        
        return jsonify(result)

    except Exception as e:
        logging.error(f"An error occurred during prediction: {e}", exc_info=True)
        return jsonify({'error': f'An unexpected server error occurred: {str(e)}'}), 500


# --- 5. Run the App Locally (for testing) ---
if __name__ == '__main__':
    logging.info("Starting Flask server on http://127.0.0.1:5000/")
    # You must run this command from the Anaconda Prompt while 'dhaka_env' is active.
    app.run(debug=True, host='0.0.0.0', port=5000)