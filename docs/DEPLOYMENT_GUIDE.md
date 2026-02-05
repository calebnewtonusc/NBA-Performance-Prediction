# Production Deployment Guide

Comprehensive guide for deploying the NBA Performance Prediction system to production environments.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling Strategies](#scaling-strategies)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers deploying the NBA Performance Prediction system for:
- **Batch Predictions**: Daily/weekly game predictions
- **Real-time API**: REST API for on-demand predictions
- **Dashboard**: Streamlit dashboard for visualization
- **Training Pipeline**: Automated model retraining

### System Requirements
- **CPU**: 2+ cores (4+ recommended)
- **RAM**: 4GB minimum (8GB+ recommended)
- **Storage**: 10GB minimum
- **Python**: 3.9+

---

## Prerequisites

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/joelnewton/NBA-Performance-Prediction.git
cd NBA-Performance-Prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-lock.txt
```

### 2. Configuration
Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```ini
# Environment
ENV=production
DEBUG=false

# API Keys (if using NBA API)
NBA_API_KEY=your_api_key_here

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/nba_predictions

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=INFO

# Model Settings
MODEL_PATH=models/production
MODEL_VERSION=v1
AUTO_RETRAIN=true
RETRAIN_SCHEDULE="0 2 * * *"  # 2 AM daily
```

---

## Deployment Options

### Option 1: Docker (Recommended)
Best for consistent environments and easy scaling.

### Option 2: Cloud Platform
Deploy to AWS, GCP, or Azure for managed infrastructure.

### Option 3: On-Premises
Deploy to your own servers with systemd services.

---

## Docker Deployment

### 1. Build Image
```bash
# Build production image
docker build -t nba-prediction:latest -f Dockerfile .

# Multi-stage build for smaller image
docker build -t nba-prediction:latest \
  --target production \
  -f Dockerfile.production .
```

### 2. Run Container
```bash
# Run dashboard
docker run -d \
  --name nba-dashboard \
  -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  nba-prediction:latest \
  streamlit run src/visualization/dashboard.py

# Run training pipeline
docker run -d \
  --name nba-training \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  nba-prediction:latest \
  python3 scripts/train_models.py --all
```

### 3. Docker Compose (Full Stack)
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  api:
    image: nba-prediction:latest
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  dashboard:
    image: nba-prediction:latest
    ports:
      - "8501:8501"
    environment:
      - ENV=production
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    command: streamlit run src/visualization/dashboard.py
    restart: unless-stopped
    depends_on:
      - api

  training:
    image: nba-prediction:latest
    environment:
      - ENV=production
      - SCHEDULE=daily
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    command: /app/scripts/scheduled_training.sh
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
      - dashboard
    restart: unless-stopped
```

Run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance
```bash
# Launch EC2 instance (Ubuntu 22.04, t3.medium or larger)
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and deploy
git clone https://github.com/joelnewton/NBA-Performance-Prediction.git
cd NBA-Performance-Prediction
docker-compose -f docker-compose.prod.yml up -d
```

#### 2. ECS (Elastic Container Service)
```bash
# Create ECR repository
aws ecr create-repository --repository-name nba-prediction

# Build and push image
$(aws ecr get-login --no-include-email)
docker build -t nba-prediction:latest .
docker tag nba-prediction:latest \
  YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nba-prediction:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nba-prediction:latest

# Create ECS task definition (see docs/aws-ecs-task.json)
aws ecs create-service --cluster nba-cluster --service-name nba-api ...
```

#### 3. Lambda (Serverless)
For batch predictions:
```python
# lambda_function.py
import json
from src.models.model_manager import ModelManager

def lambda_handler(event, context):
    manager = ModelManager()
    model = manager.load_model('game_predictions', 'production')

    # Make predictions
    predictions = model.predict(event['features'])

    return {
        'statusCode': 200,
        'body': json.dumps({'predictions': predictions.tolist()})
    }
```

### Google Cloud Platform

#### 1. Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/nba-prediction
gcloud run deploy nba-api \
  --image gcr.io/PROJECT_ID/nba-prediction \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### 2. Kubernetes (GKE) - Coming Soon
```bash
# Kubernetes deployment files are planned for future release
# For now, use Docker Compose deployment shown in Docker section
# Create cluster
# gcloud container clusters create nba-cluster \
#   --num-nodes 3 \
#   --machine-type n1-standard-2

# Deploy (files coming soon)
# kubectl apply -f deployment/kubernetes/deployment.yaml
# kubectl apply -f deployment/kubernetes/service.yaml
```

### Azure

#### 1. App Service
```bash
# Create App Service
az webapp create \
  --resource-group nba-rg \
  --plan nba-plan \
  --name nba-prediction \
  --deployment-container-image-name nba-prediction:latest
```

---

## Monitoring & Logging

### 1. Application Logging
```python
# src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler

def setup_production_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # File handler with rotation
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # JSON formatter for easy parsing
    from pythonjsonlogger import jsonlogger
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
```

### 2. Prometheus Metrics
```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions made')
prediction_duration = Histogram('prediction_duration_seconds', 'Time to make prediction')

@prediction_duration.time()
def make_prediction(features):
    prediction_counter.inc()
    # Make prediction
    ...
```

### 3. Health Checks
```python
# src/api/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "model_loaded": model_manager.is_loaded(),
        "uptime": get_uptime()
    }
```

### 4. Error Tracking (Sentry)
```python
# In your main app
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    environment="production",
    traces_sample_rate=0.1
)
```

---

## Scaling Strategies

### Horizontal Scaling
```yaml
# k8s/hpa.yaml - Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nba-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nba-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Balancing
```nginx
# nginx.conf
upstream nba_api {
    least_conn;
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://nba_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Caching
```python
# Redis caching for predictions
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379)

def get_cached_prediction(features_hash):
    cached = redis_client.get(f"pred:{features_hash}")
    if cached:
        return json.loads(cached)
    return None

def cache_prediction(features_hash, prediction, ttl=3600):
    redis_client.setex(
        f"pred:{features_hash}",
        ttl,
        json.dumps(prediction)
    )
```

---

## Security Considerations

### 1. API Authentication
```python
# src/api/auth.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

### 2. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/predict")
@limiter.limit("10/minute")
def predict(request: Request):
    ...
```

### 3. HTTPS/TLS
```bash
# Generate SSL certificate with Let's Encrypt
certbot certonly --standalone -d your-domain.com
```

### 4. Secrets Management
```bash
# Use AWS Secrets Manager, HashiCorp Vault, etc.
aws secretsmanager create-secret \
  --name nba-api-key \
  --secret-string "your-api-key"
```

---

## Troubleshooting

### Common Issues

#### 1. Out of Memory
```bash
# Increase Docker memory limit
docker run -m 4g ...

# Or in docker-compose.yml:
services:
  api:
    mem_limit: 4g
```

#### 2. Slow Predictions
- Check model size (use smaller models for real-time)
- Enable caching
- Use GPU for large models
- Optimize feature engineering

#### 3. Model Not Loading
```python
# Check model path and permissions
import os
print(f"Model exists: {os.path.exists('models/production/model.pkl')}")
print(f"Permissions: {oct(os.stat('models/production/model.pkl').st_mode)}")
```

#### 4. High CPU Usage
- Use profiling tools (see docs/PERFORMANCE_OPTIMIZATIONS.md)
- Consider horizontal scaling
- Optimize vectorized operations

---

## Maintenance

### Regular Tasks

#### Daily
- Monitor logs for errors
- Check prediction metrics
- Verify API health

#### Weekly
- Review performance metrics
- Check disk space
- Update dependencies (if needed)

#### Monthly
- Retrain models with new data
- Review and optimize queries
- Security audit

### Backup Strategy
```bash
# Backup models
tar -czf models-backup-$(date +%Y%m%d).tar.gz models/

# Backup to S3
aws s3 cp models-backup-*.tar.gz s3://your-backup-bucket/
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS ECS Guide](https://docs.aws.amazon.com/ecs/)
- [Monitoring Best Practices](https://prometheus.io/docs/practices/)

---

## Support

For deployment issues:
1. Check logs: `docker logs nba-api`
2. Review health endpoint: `curl http://localhost:8000/health`
3. Run diagnostics: `python3 scripts/validate_refactored_code.py`
4. Contact team: issues@your-domain.com
