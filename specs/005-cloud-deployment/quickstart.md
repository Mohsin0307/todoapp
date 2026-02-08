# Quickstart Guide: Advanced Cloud Deployment Todo Chatbot

## Overview
This guide provides instructions for setting up and running the event-driven Todo Chatbot application locally using Minikube, Dapr, and Redpanda.

## Prerequisites
- Docker Desktop (with Kubernetes enabled) or Minikube
- kubectl
- Dapr CLI
- Helm 3
- Node.js 20+
- Python 3.11+

## Local Setup

### 1. Start Minikube Cluster
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Install Dapr
```bash
# Install Dapr CLI if not already installed
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr on your Kubernetes cluster
dapr init -k

# Verify installation
dapr status -k
```

### 3. Install Kafka/Redpanda
```bash
# Option 1: Install Redpanda (recommended for local development)
kubectl create namespace kafka
helm repo add redpanda https://charts.redpanda.com
helm repo update
helm install redpanda redpanda/redpanda -n kafka --set resources.memory=2Gi

# Option 2: Install Kafka using Strimzi (alternative)
# Apply Strimzi operator
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
kubectl wait --for=condition=ready pod --selector=name=strimzi-cluster-operator -n kafka

# Create Kafka cluster
cat << EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
EOF
```

### 4. Set Up Dapr Components
```bash
# Create Dapr components directory
kubectl create namespace dapr-system

# Apply Dapr pubsub component
cat << EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda-0.redpanda.kafka.svc.cluster.local:9093"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "todo-consumer-group"
EOF

# Apply Dapr state store component
cat << EOF | kubectl apply -f -
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "redis-master.redis:6379"
  - name: redisPassword
    value: ""
EOF
```

### 5. Deploy Supporting Services
```bash
# Deploy Redis for state management
kubectl create namespace redis
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis -n redis --set auth.enabled=false

# Wait for Redis to be ready
kubectl wait --for=condition=ready pod --selector=app.kubernetes.io/name=redis -n redis
```

### 6. Prepare Application Configuration
```bash
# Create secrets and configmaps
kubectl create secret generic todo-secrets \
  --from-literal=DATABASE_URL="postgresql://username:password@neon-host:5432/dbname" \
  --from-literal=JWT_SECRET="your-jwt-secret" \
  --from-literal=OPENAI_API_KEY="your-openai-key"

kubectl create configmap todo-config \
  --from-literal=APP_ENV="development" \
  --from-literal=DAPR_SIDECAR_NAME="todo-dapr-sidecar"
```

### 7. Build and Deploy Application
```bash
# Build Docker images
cd backend
docker build -t todo-backend:latest .
cd ../frontend
docker build -t todo-frontend:latest .

# Push images to registry (use minikube registry for local)
eval $(minikube docker-env)
docker build -t todo-backend:latest .
docker build -t todo-frontend:latest .

# Deploy using Kubernetes manifests or Helm
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

### 8. Deploy Using Helm (Alternative Method)
```bash
# Update Helm dependencies
cd helm/todo-chatbot
helm dependency update

# Install the application
helm install todo-chatbot . \
  --namespace default \
  --create-namespace \
  --set image.backend.tag=latest \
  --set image.frontend.tag=latest \
  --set database.url="postgresql://username:password@neon-host:5432/dbname" \
  --set openai.apiKey="your-openai-key"
```

## Access the Application
```bash
# Port forward to access the frontend
kubectl port-forward svc/todo-frontend 3000:80

# Access the Dapr dashboard
dapr dashboard -k

# Check application status
kubectl get pods
kubectl get services
dapr list
```

## Verify Event-Driven Architecture
```bash
# Check Kafka/Redpanda topics
kubectl exec -it redpanda-0 -n kafka -- rpk topic list

# Monitor Dapr sidecar logs
kubectl logs deployment/todo-backend-dapr

# Verify event processing
kubectl get pods --selector=app=todo-processor
```

## Local Development Workflow
```bash
# Watch for changes and rebuild
# Backend: uvicorn main:app --reload
# Frontend: npm run dev

# For Kubernetes development, use Skaffold or Tilt for hot reloading
skaffold dev --port-forward
```

## Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/

# Run frontend tests
cd frontend
npm test

# Run integration tests
kubectl exec -it deployment/todo-backend -- python -m pytest tests/integration/
```

## Troubleshooting
1. **Pod stuck in Pending**: Check resource availability in Minikube
   ```bash
   minikube ssh
   df -h  # Check disk space
   free -h  # Check memory
   ```

2. **Dapr sidecar not starting**: Check Dapr installation and components
   ```bash
   dapr status -k
   kubectl describe pod <pod-name>
   ```

3. **Kafka connection issues**: Verify broker address and network connectivity
   ```bash
   kubectl exec -it redpanda-0 -n kafka -- rpk cluster info
   kubectl logs -f -n kafka -l app=redpanda
   ```

4. **Database connectivity**: Check if Neon database is accessible
   ```bash
   kubectl exec -it deployment/todo-backend -- nc -zv neon-host 5432
   ```

## Scaling
```bash
# Scale backend services
kubectl scale deployment todo-backend --replicas=3

# Enable HPA based on CPU
kubectl autoscale deployment todo-backend --cpu-percent=70 --min=1 --max=10
```

## Cleanup
```bash
# Uninstall application
helm uninstall todo-chatbot -n default

# Remove Dapr
dapr uninstall -k

# Stop Minikube
minikube stop

# Delete Minikube cluster (optional)
minikube delete
```

## Next Steps
1. Set up monitoring and logging with Prometheus and Grafana
2. Implement CI/CD pipeline with GitHub Actions
3. Deploy to production Kubernetes cluster
4. Set up managed Kafka service in production