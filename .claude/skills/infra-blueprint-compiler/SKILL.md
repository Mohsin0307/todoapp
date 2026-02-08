---
name: infra-blueprint-compiler
description: Convert infrastructure specifications into repeatable Kubernetes deployment blueprints
version: 1.0.0
---

# Infra-Blueprint-Compiler

## When to Use

Use this skill when you need to:
- Convert infrastructure specifications into structured Kubernetes deployment blueprints
- Generate reproducible deployment configurations from infrastructure requirements
- Automate the creation of infrastructure-as-code artifacts based on specs
- Transform high-level infrastructure designs into concrete deployment steps
- Ensure consistency across multiple environment deployments

## Procedure

1. **Read Infrastructure Spec**
   - Parse the provided infrastructure specification document
   - Extract service definitions, resource requirements, and configuration parameters
   - Identify networking requirements and security constraints

2. **Identify Services and Dependencies**
   - Map out all required services and their interdependencies
   - Determine service relationships (client-server, microservices, etc.)
   - Identify external dependencies and third-party integrations

3. **Select Deployment Strategy**
   - Choose appropriate deployment patterns (rolling updates, blue-green, etc.)
   - Determine resource allocation based on requirements
   - Select suitable storage and networking configurations

4. **Generate Deployment Artifacts**
   - Create Kubernetes manifests (Deployments, Services, ConfigMaps, etc.)
   - Generate necessary configuration files and environment variables
   - Produce deployment scripts and operational procedures

## Output Format

The skill produces a structured output containing:

- **Deployment Manifests**: Kubernetes YAML files for each service
- **Configuration Files**: Environment-specific configurations
- **Service Dependencies Map**: Visual/text representation of service relationships
- **Deployment Steps**: Sequential instructions for deploying the infrastructure
- **Validation Checks**: Pre-deployment and post-deployment validation procedures

Each output component follows deterministic patterns based solely on the input specification, with no additional assumptions made beyond what is explicitly defined in the infrastructure spec.