---
name: k8s-deployer-lite
description: Local Kubernetes operations for deploying, scaling, debugging, and validating services using kubectl-ai and Minikube
version: 1.0.0
---

# k8s-deployer-lite

Lightweight Kubernetes deployment skill for local Minikube environments using AI-assisted tools.

## When to Use

Use this skill when you need to:
- Deploy applications to local Minikube clusters
- Scale deployments up/down
- Debug pod failures and service issues
- Validate Kubernetes resources
- Perform routine kubectl operations with AI assistance
- Apply manifests or Helm releases locally

## Procedure

1. **Validate Cluster State**
   - Check if Minikube is running with `minikube status`
   - Verify kubectl can connect to the cluster

2. **Apply Resources**
   - Use `kubectl-ai apply -f <manifest>` when available
   - Fall back to `kubectl apply -f <manifest>` if AI tool unavailable
   - For Helm: `helm upgrade --install <release> <chart>`

3. **Scale Deployments**
   - Use `kubectl-ai scale deployment/<name> --replicas=<count>` when available
   - Fall back to `kubectl scale deployment/<name> --replicas=<count>`

4. **Inspect Issues**
   - Use `kubectl-ai get pods` and `kubectl-ai describe pod <name>` when available
   - Fall back to standard kubectl equivalents
   - Check logs with `kubectl-ai logs <pod>` or `kubectl logs <pod>`

5. **Validate Operations**
   - Confirm resource status with appropriate get commands
   - Verify expected replica counts and readiness

## Output Format

- Short, command-focused responses
- Success/failure status for each operation
- Relevant resource identifiers (pod names, deployment names)
- Error messages when operations fail
- Resource counts and status summaries

## Constraints

- Use kubectl-ai when possible, fall back to kubectl if AI tool unavailable
- No destructive operations affecting the entire cluster
- Focus on targeted resource management
- Keep responses concise and action-oriented
- Preserve existing cluster state outside target resources