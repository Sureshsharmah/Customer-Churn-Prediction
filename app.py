from flask import Flask, render_template, request, jsonify
import pandas as pd
from joblib import load
import numpy as np
import sklearn

app = Flask(__name__)

model = load('lr_churn_model.joblib')
print("Model loaded successfully!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'gender': request.form['gender'],
            'SeniorCitizen': request.form['seniorCitizen'],
            'Partner': request.form['partner'],
            'Dependents': request.form['dependents'],
            'tenure': int(request.form['tenure']),
            'PhoneService': request.form['phoneService'],
            'MultipleLines': request.form['multipleLines'],
            'InternetService': request.form['internetService'],
            'OnlineSecurity': request.form['onlineSecurity'],
            'OnlineBackup': request.form['onlineBackup'],
            'DeviceProtection': request.form['deviceProtection'],
            'TechSupport': request.form['techSupport'],
            'StreamingTV': request.form['streamingTV'],
            'StreamingMovies': request.form['streamingMovies'],
            'Contract': request.form['contract'],
            'PaperlessBilling': request.form['paperlessBilling'],
            'PaymentMethod': request.form['paymentMethod'],
            'MonthlyCharges': float(request.form['monthlyCharges']),
            'TotalCharges': float(request.form['totalCharges']),
            'TenureGroup': request.form['tenureGroup'],
            'HasInternetService': request.form['hasInternetService'],
            'MultipleServices': request.form['multipleServices']
        }

        df = pd.DataFrame([data])
        probabilities = model.predict_proba(df)[0]
        churn_prob = probabilities[1]
        not_churn_prob = probabilities[0]

        if churn_prob >= 0.5:
            prediction = 'Churn'
            display_prob = churn_prob
            confidence = 'high' if churn_prob > 0.7 else 'medium'
        else:
            prediction = 'Not Churn'
            display_prob = not_churn_prob
            confidence = 'low'

        if (data['Contract'] == 'Month-to-month' and 
            data['tenure'] < 3 and 
            churn_prob < 0.7):
            prediction = 'Churn'
            display_prob = max(churn_prob, 0.7)
            confidence = 'high'
            override = True

        result = {
            'prediction': prediction,
            'probability': round(display_prob * 100, 2),
            'confidence': confidence,
            'probabilities': {
                'churn': round(churn_prob * 100, 2),
                'not_churn': round(not_churn_prob * 100, 2)
            }
        }

        print(f"Raw probabilities: Churn {churn_prob:.2f}, Not Churn {not_churn_prob:.2f}")
        print(f"Final prediction: {result}")

        return render_template('index.html', prediction=result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'Please check your input values'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)