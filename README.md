🔮 Telco Churn Prediction + MLOps Pipeline
End-to-end solution from EDA to Kubernetes deployment

🛠️ Full Tech Stack
Category	Tools Used
Data Science	Pandas, NumPy, Matplotlib/Seaborn, Jupyter, Scikit-learn
ML/DL	XGBoost, TensorFlow/Keras (Neural Nets), SHAP, Feature-engine
API	FastAPI (with Swagger docs), Flask (alternate), Uvicorn
Infra	Docker, Docker-compose, Kubernetes (minikube), Prometheus+Grafana
Dev Tools	VS Code, Git, GitHub Actions, pytest, Black (formatting)
🚀 How to Run
Option 1: Local Development (VS Code)
bash

Run Data Science Pipeline (Jupyter)

Problem Statement 1: Data Science Task
python -m venv venv
venv\Scripts\activate
cd telco-churn-project
cd model_development
pip install -r requirements.txt
python app.py

Problem Statement 2: MLOps Task 
cd telco-churn-project
cd mlops_deployment
pip install -r requirements.txt
cd app
# 3. Run FastAPI locally
uvicorn api.main:app --reload
will be directed to - http://localhost:8000/docs

# 4. Run Docker
# Check Docker version (confirms Docker is installed)
docker --version

# Verify Docker is running
docker info

# List running containers (should be empty if nothing is running)
docker ps

# List available Docker images
docker images

Build your Docker image
# Build the image with tag 'churn-prediction'
docker build -t churn-prediction .

# Run the container, mapping port 5000 (host) to 5000 (container)
docker run -p 5000:5000 churn-prediction

# List running containers
docker ps

# Check logs (if running in detached mode)
docker logs churn-app

# Stop the container (if running in foreground, use Ctrl+C)
docker stop churn-app

# Remove the container (optional)
docker rm churn-app


# 1. Clone and setup
git clone [https://github.com/Sureshsharmah/telco-churn.git](https://github.com/Sureshsharmah/Customer-Churn-Prediction)
cd telco-churn
python -m venv venv && source venv/bin/activate  
pip install -r requirements.txt

# 2. Launch Jupyter notebook for EDA
jupyter notebook notebooks/churn_analysis.ipynb



Option 2: Docker Production
# Build and run with monitoring
docker-compose up -d  # Includes:
                      # - API (FastAPI on :8000)
                      # - Prometheus (metrics on :9090)
                      # - Grafana (dashboards on :3000)
Option 3: Kubernetes (minikube)
bash
kubectl apply -f k8s/deployment.yaml  # Deploys:
                                      # - API service
                                      # - Model monitoring
                                      # - Auto-scaling
🌟 Key Features
95% AUC-ROC model with business rule overrides

VS Code devcontainer pre-configured

CI/CD: GitHub Actions for auto-testing + Docker Hub pushes

Infra-as-Code: Kubernetes manifests included




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
