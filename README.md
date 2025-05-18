## Production Scaling

### Option 1: Kubernetes
1. Create deployment.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-predictor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: churn-predictor
  template:
    metadata:
      labels:
        app: churn-predictor
    spec:
      containers:
      - name: churn-predictor
        image: yourusername/churn-predictor:latest
        ports:
        - containerPort: 8000


# Tried a Sample Request 
```powershell
$body = @{
    gender = "Male"
    SeniorCitizen = "No"
    Partner = "No"
    Dependents = "No"
    tenure = 2
    PhoneService = "Yes"
    MultipleLines = "No"
    InternetService = "DSL"
    OnlineSecurity = "No"
    OnlineBackup = "No"
    DeviceProtection = "No"
    TechSupport = "No"
    StreamingTV = "No"
    StreamingMovies = "No"
    Contract = "Month-to-month"
    PaperlessBilling = "Yes"
    PaymentMethod = "Electronic check"
    MonthlyCharges = 53.85
    TotalCharges = 108.15
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method Post -Body $body -ContentType "application/json"