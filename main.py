from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from joblib import load
import os
import pandas as pd
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Telco Churn Prediction API",
             description="API for predicting customer churn with business rule overrides",
             version="1.0.0")

model_path = os.path.join(os.path.dirname(__file__), 'models', 'lr_churn_model.joblib')
model = load(model_path)

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: str
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float
    TenureGroup: Optional[str] = None
    HasInternetService: Optional[str] = None
    MultipleServices: Optional[str] = None

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "version": "1.0.0"
    }

@app.post("/predict")
async def predict(data: CustomerData):
    try:
        input_data = data.dict()
        
        if input_data['TenureGroup'] is None:
            input_data['TenureGroup'] = get_tenure_group(input_data['tenure'])
        
        if input_data['HasInternetService'] is None:
            input_data['HasInternetService'] = 'Yes' if input_data['InternetService'] != 'No' else 'No'
        
        if input_data['MultipleServices'] is None:
            input_data['MultipleServices'] = 'Yes' if (input_data['PhoneService'] == 'Yes' and 
                                                     input_data['InternetService'] != 'No') else 'No'
        
        df = pd.DataFrame([input_data])
        
        probabilities = model.predict_proba(df)[0]
        churn_prob = probabilities[1]
        not_churn_prob = probabilities[0]
        
        is_high_risk = (
            input_data['Contract'] == 'Month-to-month' and
            input_data['tenure'] < 6 and
            input_data['InternetService'] in ['Fiber optic', 'DSL']
        )
        
        if is_high_risk and churn_prob < 0.6:
            churn_prob = min(0.9, churn_prob + 0.3)
            override_applied = True
        else:
            override_applied = False
        
        if churn_prob >= 0.5:
            prediction = "Churn"
            display_prob = churn_prob
            confidence = "high" if churn_prob > 0.75 else "medium"
        else:
            prediction = "Not Churn"
            display_prob = not_churn_prob
            confidence = "low"
        
        return {
            "prediction": prediction,
            "probability": round(display_prob * 100, 2),
            "confidence": confidence,
            "risk_analysis": {
                "is_high_risk": is_high_risk,
                "risk_factors": [
                    f"Short tenure ({input_data['tenure']} months)",
                    f"{input_data['Contract']} contract",
                    f"{input_data['InternetService']} service"
                ],
                "business_override_applied": override_applied,
                "original_probability": round(probabilities[1] * 100, 2) if override_applied else None
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction failed: {str(e)}"
        )

def get_tenure_group(tenure: int) -> str:
    if tenure <= 12:
        return "0-12"
    elif tenure <= 24:
        return "12-24"
    elif tenure <= 36:
        return "24-36"
    elif tenure <= 48:
        return "36-48"
    elif tenure <= 60:
        return "48-60"
    else:
        return "60+"