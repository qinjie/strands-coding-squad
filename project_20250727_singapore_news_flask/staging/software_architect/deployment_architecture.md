# Deployment Architecture - Singapore News Flask Application

## Overview

This document outlines the deployment architecture for the Singapore News Flask application. The architecture is designed to be scalable, reliable, and maintainable while meeting the performance requirements for approximately 10,000 users.

## Deployment Strategy

The application will follow a containerized deployment strategy using Docker, which provides:

1. **Consistency**: Same environment across development, testing, and production
2. **Isolation**: Application and dependencies are isolated from the host system
3. **Scalability**: Easy horizontal scaling by adding more containers
4. **Portability**: Deploy to any environment that supports Docker
5. **Version Control**: Container images are versioned for reliable deployments

## Infrastructure Requirements

### Minimum Requirements (Development/Testing)

| Resource      | Specification                                |
|---------------|----------------------------------------------|
| CPU           | 2 vCPUs                                      |
| Memory        | 4 GB RAM                                     |
| Storage       | 20 GB SSD                                    |
| Network       | 100 Mbps                                     |
| Operating System | Linux (Ubuntu 22.04 LTS recommended)      |

### Production Requirements (10,000 users)

| Resource      | Specification                                |
|---------------|----------------------------------------------|
| CPU           | 4 vCPUs                                      |
| Memory        | 8 GB RAM                                     |
| Storage       | 50 GB SSD                                    |
| Network       | 1 Gbps                                       |
| Operating System | Linux (Ubuntu 22.04 LTS recommended)      |

## Deployment Architecture Diagram

### Development Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Compose Environment                  │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Flask App      │  │  Redis Cache    │  │  PostgreSQL DB  │  │
│  │  Container      │  │  Container      │  │  Container      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Production Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                        Load Balancer                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
┌───────────────▼───────────┐   ┌───────────────▼───────────┐
│  Web Server Container 1   │   │  Web Server Container 2   │
│  ┌─────────────────────┐  │   │  ┌─────────────────────┐  │
│  │      Nginx          │  │   │  │      Nginx          │  │
│  └──────────┬──────────┘  │   │  └──────────┬──────────┘  │
│             │             │   │             │             │
│  ┌──────────▼──────────┐  │   │  ┌──────────▼──────────┐  │
│  │     Gunicorn        │  │   │  │     Gunicorn        │  │
│  └──────────┬──────────┘  │   │  └──────────┬──────────┘  │
│             │             │   │             │             │
│  ┌──────────▼──────────┐  │   │  ┌──────────▼──────────┐  │
│  │    Flask App        │  │   │  │    Flask App        │  │
│  └─────────────────────┘  │   │  └─────────────────────┘  │
└───────────────────────────┘   └───────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                │
                ┌───────────────▼───────────────┐
                │      Redis Cache Cluster      │
                └───────────────────────────────┘
                                │
                ┌───────────────▼───────────────┐
                │     PostgreSQL Database       │
                └───────────────────────────────┘
```

## Container Configuration

### Flask Application Container

```dockerfile
# Dockerfile for Flask application
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run Gunicorn with 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Nginx Container

```dockerfile
# Dockerfile for Nginx
FROM nginx:1.24-alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configuration
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Nginx configuration:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://flask-app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 1d;
    }
}
```

## Docker Compose Configuration

### Development Environment

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  flask-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - NEWSAPI_KEY=${NEWSAPI_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    command: flask run --host=0.0.0.0

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

### Production Environment

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    build:
      context: ./nginx
    ports:
      - "80:80"
    depends_on:
      - flask-app

  flask-app:
    build: .
    expose:
      - "5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=production
      - NEWSAPI_KEY=${NEWSAPI_KEY}
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/newsapp
    depends_on:
      - redis
      - db

  redis:
    image: redis:7.2-alpine
    volumes:
      - redis-data:/data

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=newsapp

volumes:
  redis-data:
  postgres-data:
```

## Deployment Environments

### Local Development

Developers can run the application locally using Docker Compose:

```bash
# Set environment variables
export NEWSAPI_KEY=your_api_key

# Start the development environment
docker-compose -f docker-compose.dev.yml up
```

### Testing/Staging Environment

The staging environment mirrors the production setup but with reduced resources:

1. Deploy using the production Docker Compose file
2. Use a separate NewsAPI key for testing
3. Implement feature flags for testing new features

### Production Environment

The production deployment can be done on:

1. **Cloud Provider** (Recommended):
   - AWS Elastic Container Service (ECS)
   - Google Cloud Run
   - Azure Container Instances
   - Digital Ocean App Platform

2. **Self-Hosted**:
   - Kubernetes cluster
   - Docker Swarm
   - Single server with Docker Compose

## Continuous Integration/Continuous Deployment (CI/CD)

The application will use a CI/CD pipeline for automated testing and deployment:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Code Push  │────►│   CI Tests  │────►│  Build and  │────►│  Deploy to  │
│  to GitHub  │     │             │     │  Push Image │     │  Production │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### CI/CD Pipeline Steps

1. **Code Push**: Developer pushes code to GitHub repository
2. **Automated Tests**: Run unit tests, integration tests, and linting
3. **Build Docker Image**: Build the application Docker image
4. **Push to Registry**: Push the image to a container registry
5. **Deploy**: Deploy the new image to the target environment

Example GitHub Actions workflow:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      - name: Test with pytest
        run: |
          pytest --cov=./ --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: username/singapore-news-flask:latest
      - name: Deploy to production
        run: |
          # Deployment script or command
          echo "Deploying to production..."
```

## Scaling Strategy

### Vertical Scaling

Increase resources (CPU, memory) for the application containers:

1. Adjust container resource limits in Docker Compose or Kubernetes
2. Increase instance size on cloud providers

### Horizontal Scaling

Add more application instances to handle increased load:

1. Add more Flask application containers
2. Configure load balancer to distribute traffic
3. Ensure session persistence if needed

### Database Scaling

1. **Read Replicas**: Add read replicas for PostgreSQL
2. **Connection Pooling**: Implement PgBouncer for connection management
3. **Sharding**: Partition data across multiple database instances (if needed)

### Cache Scaling

1. **Redis Cluster**: Implement Redis Cluster for distributed caching
2. **Cache Optimization**: Tune cache TTL based on data volatility
3. **Memory Management**: Configure Redis memory policies

## Monitoring and Observability

### Metrics Collection

1. **Application Metrics**: Response time, error rate, request count
2. **System Metrics**: CPU, memory, disk usage
3. **Cache Metrics**: Hit rate, memory usage
4. **Database Metrics**: Query performance, connection count

### Logging

1. **Centralized Logging**: Aggregate logs from all containers
2. **Structured Logging**: Use JSON format for machine-readable logs
3. **Log Levels**: Configure appropriate log levels for each environment

### Alerting

1. **Performance Alerts**: Notify when response time exceeds thresholds
2. **Error Rate Alerts**: Notify when error rate increases
3. **Resource Alerts**: Notify when resources are near capacity
4. **API Quota Alerts**: Notify when approaching NewsAPI limits

## Backup and Disaster Recovery

### Database Backups

1. **Regular Backups**: Daily automated backups
2. **Point-in-Time Recovery**: Transaction log backups
3. **Backup Testing**: Regular restoration tests

### Disaster Recovery Plan

1. **Recovery Time Objective (RTO)**: Maximum acceptable downtime (e.g., 1 hour)
2. **Recovery Point Objective (RPO)**: Maximum acceptable data loss (e.g., 15 minutes)
3. **Failover Procedure**: Documented steps for failover
4. **Regular Testing**: Conduct disaster recovery drills

## Cost Optimization

### Resource Optimization

1. **Right-sizing**: Use appropriate instance sizes
2. **Auto-scaling**: Scale resources based on demand
3. **Spot Instances**: Use spot instances for non-critical components

### Caching Strategy

1. **Aggressive Caching**: Cache NewsAPI responses to reduce API calls
2. **Browser Caching**: Configure appropriate cache headers for static assets
3. **CDN**: Use a Content Delivery Network for static assets

## Deployment Checklist

Before deploying to production:

1. **Security Scan**: Check for vulnerabilities in code and dependencies
2. **Performance Testing**: Verify application performance under load
3. **Configuration Review**: Ensure all environment variables are set
4. **Backup Verification**: Verify backup and restore procedures
5. **Monitoring Setup**: Confirm monitoring and alerting are configured
6. **Documentation**: Update deployment documentation

## Conclusion

This deployment architecture provides a scalable, reliable, and maintainable solution for the Singapore News Flask application. By following containerization best practices and implementing proper monitoring, the application can handle the expected user load while maintaining good performance and reliability.