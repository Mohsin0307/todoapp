# Data Model: Phase IV - Cloud Native Todo Chatbot Deployment

## Entities

### Kubernetes Deployment
- **name**: Unique identifier for the deployment
- **replicas**: Number of pod instances to maintain
- **image**: Container image reference with tag
- **ports**: List of exposed ports
- **environment**: Key-value pairs for configuration
- **resources**: CPU and memory limits/requests
- **healthChecks**: Liveness and readiness probe configurations

### Service Configuration
- **name**: Unique identifier for the service
- **type**: Service type (ClusterIP, NodePort, LoadBalancer)
- **selector**: Labels to match pods
- **ports**: Port mappings from service to pods
- **externalTrafficPolicy**: Traffic routing policy

### Helm Chart Values
- **appName**: Name of the application
- **image**: Image repository and tag
- **replicaCount**: Number of desired pod replicas
- **service**: Service configuration parameters
- **resources**: Resource limits and requests
- **nodeSelector**: Node selection constraints
- **tolerations**: Taint tolerations for scheduling

### Docker Image Configuration
- **imageName**: Name of the Docker image
- **buildContext**: Path to build context
- **dockerfile**: Path to Dockerfile (if non-standard)
- **tags**: List of tags to apply to image
- **buildArgs**: Arguments to pass during build

### AI-Assisted Operation
- **operationType**: Type of operation (deploy, scale, debug, etc.)
- **targetResource**: Resource to operate on
- **parameters**: Operation-specific parameters
- **aiTool**: AI tool to use (kubectl-ai, kagent, Docker AI)
- **fallbackCommand**: Manual command if AI tool unavailable

## Relationships
- One Helm Chart Values entity defines configuration for multiple Kubernetes Deployment entities
- One Kubernetes Deployment entity corresponds to one Docker Image Configuration
- Multiple AI-Assisted Operation entities may act on a single Kubernetes Deployment entity
- Service Configuration entities reference Kubernetes Deployment entities via selectors