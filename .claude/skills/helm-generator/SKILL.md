---
name: helm-generator
description: Generate Helm charts for deploying microservices on Minikube with standard best practices
version: 1.0.0
---

# Helm Chart Generator

## When to Use

Use this skill when you need to generate Helm charts for deploying containerized microservices (frontend or backend applications) on Kubernetes clusters, particularly Minikube. This skill is appropriate for:

- Containerizing existing frontend/backend applications for Kubernetes deployment
- Generating standardized Helm charts following best practices
- Creating deployment manifests with proper resource configuration
- Setting up scalable deployments with configurable replica counts
- Adding resource limits and requests for production readiness

## Procedure

1. Analyze the service type (frontend or backend) to determine specific requirements
2. Generate a Chart.yaml file with appropriate metadata
3. Create a values.yaml file with configurable parameters:
   - Image repository and tag
   - Replica count settings
   - Resource limits and requests
   - Service configuration
4. Generate deployment template with:
   - Proper labels and selectors
   - Configurable resource constraints
   - Environment variables handling
5. Create service template for internal cluster communication
6. Ensure compatibility with Kubernetes v1.27 standards
7. Validate proper namespace scoping and label consistency

## Output Format

The skill generates a standard Helm chart structure:

```
chart-name/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl
└── charts/
```

### Chart.yaml contains:
- Name and version of the chart
- Description of the service
- API version specification

### values.yaml includes:
- Image configuration (repository, tag, pull policy)
- Service settings (type, port)
- Replica count configuration
- Resource limits and requests
- Node selector and tolerations (optional)

### Templates provide:
- Deployment manifest with configurable parameters
- Service definition for cluster networking
- Helper templates for consistent labeling

The generated charts will follow Kubernetes v1.27 compatibility standards, include proper resource management, and exclude ingress configurations by default to maintain simplicity.