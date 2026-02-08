# Quickstart Guide: Phase IV - Cloud Native Todo Chatbot Deployment

## Prerequisites

1. **Install Minikube**
   ```bash
   # Install minikube (macOS)
   brew install minikube

   # Install minikube (Windows with Chocolatey)
   choco install minikube

   # Install minikube (Linux)
   curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
   && chmod +x minikube && sudo mv minikube /usr/local/bin/
   ```

2. **Install kubectl**
   ```bash
   # Install kubectl (macOS)
   brew install kubectl

   # Install kubectl (Windows with Chocolatey)
   choco install kubernetes-cli

   # Install kubectl (Linux)
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

3. **Install Helm**
   ```bash
   # Install Helm (macOS)
   brew install helm

   # Install Helm (Windows with Chocolatey)
   choco install kubernetes-helm

   # Install Helm (Linux)
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

4. **Install Docker**
   - Download and install Docker Desktop from https://www.docker.com/products/docker-desktop

## AI-Assisted Tools Setup

1. **Enable Docker AI Agent (Gordon)** (if available)
   - Check if Docker AI features are enabled in Docker Desktop settings
   - Verify with: `docker --help` and look for AI-related commands

2. **kubectl-ai Setup** (if available)
   - Install kubectl-ai plugin if available in your environment
   - Verify with: `kubectl ai version` (if installed)

## Start Minikube Cluster

```bash
# Start minikube with Docker driver
minikube start --driver=docker

# Verify cluster is running
kubectl cluster-info

# Verify kubectl connection
kubectl get nodes
```

## Build Container Images

```bash
# Navigate to project root
cd /path/to/todo-chatbot

# Build frontend image
docker build -t todo-chatbot-frontend:latest -f docker/Dockerfile.frontend .

# Build backend image
docker build -t todo-chatbot-backend:latest -f docker/Dockerfile.backend .

# Tag images for minikube
docker tag todo-chatbot-frontend:latest minikube/todo-chatbot-frontend:latest
docker tag todo-chatbot-backend:latest minikube/todo-chatbot-backend:latest
```

## Deploy with Helm

```bash
# Navigate to helm directory
cd helm/todo-chatbot

# Install the chart
helm install todo-chatbot . --values values-dev.yaml

# Verify deployment
kubectl get pods
kubectl get services

# Get the application URL
minikube service todo-chatbot-frontend --url
```

## Using AI-Assisted Commands

```bash
# Use kubectl-ai for deployment operations (if available)
kubectl ai "show me the status of all pods"
kubectl ai "scale the frontend deployment to 3 replicas"

# Use kubectl-ai for troubleshooting (if available)
kubectl ai "what's wrong with the backend pod?"
```

## Access the Application

```bash
# Get the service URL
minikube service todo-chatbot-frontend

# Or get the URL without opening browser
minikube service todo-chatbot-frontend --url
```

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-chatbot

# Stop minikube
minikube stop

# Optionally delete the cluster
minikube delete
```