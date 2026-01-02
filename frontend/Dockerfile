# Frontend Dockerfile - Next.js Application
# Node 18 with Alpine base for smaller image size

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies for node-gyp and Next.js
RUN apk add --no-cache libc6-compat curl

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Default command (can be overridden in docker-compose.yml)
CMD ["npm", "run", "dev"]
