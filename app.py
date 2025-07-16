from flask import Flask, request, jsonify
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load saved models
rf = joblib.load('rf_model.pkl')
ridge = joblib.load('ridge_model.pkl')

@app.route('/')
def home():
    return "Gold Price Prediction API is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Expect JSON payload like: {"features": [val1, val2, ..., val9]}
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)

        # Predict from both models
        pred_rf = rf.predict(features)[0]
        pred_ridge = ridge.predict(features)[0]

        # Average the predictions
        predicted_price = round((pred_rf + pred_ridge) / 2, 2)

        return jsonify({
            'predicted_price': predicted_price
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
