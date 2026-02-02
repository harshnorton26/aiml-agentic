# 🐳 Docker Setup Guide - HR Policy Assistant

## Overview

This application can be easily deployed using Docker and Docker Compose. The setup includes:

- **Frontend**: Streamlit UI (Port 8501)
- **Backend**: Python application with LangChain
- **LLM Service**: Ollama with Mistral model (Port 11434)
- **Networking**: Docker network for inter-service communication

## Prerequisites

1. **Docker Desktop** installed ([Download](https://www.docker.com/products/docker-desktop))
2. **Docker Compose** (included with Docker Desktop)
3. Minimum **8GB RAM** recommended (for Ollama + Mistral)
4. **10GB free disk space** (for Mistral model)

## Quick Start

### 1️⃣ **Build and Run with Docker Compose**

```bash
cd h:\aiml\agentic
docker-compose up --build
```

This will:
- Build the HR Policy Assistant image
- Start Ollama service
- Pull the Mistral model (~5GB - first time only)
- Start the Streamlit application
- Create a Docker network for communication

### 2️⃣ **Access the Application**

Once running, open your browser and go to:
```
http://localhost:8501
```

## Docker Compose Services

### Service 1: Ollama (LLM Server)
```yaml
Service: ollama
Container: ollama-mistral
Port: 11434
Model: Mistral
```

**Health Check**: Checks if Ollama is responding to API calls

**Volume**: `ollama_data` - Persists downloaded models

### Service 2: HR Policy Assistant (Frontend)
```yaml
Service: app
Container: hr-policy-assistant
Port: 8501
Framework: Streamlit
```

**Dependencies**: Waits for Ollama to be healthy

**Volumes**: Mounts for hot-reloading during development

## File Structure

```
h:\aiml\agentic\
├── Dockerfile           # Application image definition
├── docker-compose.yml   # Multi-service orchestration
├── .dockerignore        # Files to exclude from Docker build
├── DOCKER_SETUP.md      # This file
├── frontend/
│   └── app.py
├── backend/
│   ├── hr_agent.py
│   ├── tools.py
│   └── prompts.py
├── data/
│   └── policies/
└── requirements.txt
```

## Common Commands

### Start Services
```bash
# Start in foreground (see logs)
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Rebuild images
docker-compose up --build

# Rebuild without cache
docker-compose up --build --no-cache
```

### Stop Services
```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

### View Logs
```bash
# View logs from all services
docker-compose logs

# View logs from specific service
docker-compose logs ollama
docker-compose logs app

# Follow logs in real-time
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Check Status
```bash
# List running containers
docker-compose ps

# View service details
docker-compose ps -a
```

### Interactive Access
```bash
# Open shell in Streamlit container
docker-compose exec app bash

# Open shell in Ollama container
docker-compose exec ollama bash

# View Ollama models
docker-compose exec ollama ollama list
```

## Troubleshooting

### Issue: "Ollama connection failed"

**Solution**: Wait for Ollama to fully start and pull the Mistral model
```bash
# Check Ollama logs
docker-compose logs ollama

# Wait 2-3 minutes on first startup for model download
```

### Issue: "Port 8501 already in use"

**Solution**: Change the port in docker-compose.yml
```yaml
# In docker-compose.yml, change:
ports:
  - "8501:8501"  # Change first port to available one
# To:
ports:
  - "8502:8501"  # Now access at localhost:8502
```

### Issue: "Not enough disk space"

**Solution**: Free up space or increase Docker's allocated disk
- Mistral model is ~5GB
- Docker images and containers need ~2-3GB
- Total: ~10GB minimum

### Issue: Container keeps restarting

**Solution**: Check health checks and logs
```bash
docker-compose logs app
docker-compose logs ollama
```

## Advanced Configuration

### Environment Variables

Create `.env` file to customize:
```env
# Ollama settings
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=mistral

# Streamlit settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

### Custom Model

To use a different Ollama model, edit `docker-compose.yml`:
```yaml
ollama:
  command: sh -c "ollama pull llama2 && ollama serve"
  # Change 'mistral' to: llama2, llama3, neural-chat, etc.
```

Then update `backend/hr_agent.py`:
```python
self.llm = Ollama(
    model="llama2",  # Change model name
    base_url="http://ollama:11434",
)
```

### Persistent Data

To persist policy documents and configuration:
```yaml
volumes:
  app:
    image: hr-policy-assistant:latest
    volumes:
      # Named volumes for persistence
      - app_data:/app/data
      - app_config:/app/config

volumes:
  app_data:
    driver: local
  app_config:
    driver: local
```

## Deployment

### Production Deployment

For production, consider:

1. **Use specific image versions**
   ```dockerfile
   FROM python:3.11-slim
   FROM ollama/ollama:0.1.21
   ```

2. **Add resource limits**
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '2.0'
             memory: 2G
           reservations:
             cpus: '1.0'
             memory: 1G
   ```

3. **Add restart policies**
   ```yaml
   services:
     app:
       restart_policy:
         condition: on-failure
         delay: 5s
         max_attempts: 5
   ```

4. **Use environment file**
   ```bash
   docker-compose --env-file .env.production up -d
   ```

### Docker Hub (Optional)

Push image to Docker Hub:
```bash
# Build image
docker build -t harshnorton26/hr-policy-assistant:latest .

# Login to Docker Hub
docker login

# Push
docker push harshnorton26/hr-policy-assistant:latest

# Pull and run anywhere
docker run -p 8501:8501 harshnorton26/hr-policy-assistant:latest
```

## Performance Tips

1. **Use named volumes** for better performance than bind mounts
2. **Allocate sufficient Docker resources** (CPU: 4+, Memory: 8GB+)
3. **Use `.dockerignore`** to exclude unnecessary files
4. **Cache layers** - Put frequently changing files at end of Dockerfile
5. **Multi-stage builds** - Reduce final image size

## Network Architecture

```
┌─────────────────────────────────────┐
│      Docker Network (Bridge)        │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────────┐               │
│  │  Streamlit App   │               │
│  │  (Port 8501)     │──┐            │
│  └──────────────────┘  │            │
│                        │            │
│  ┌──────────────────┐  │            │
│  │  Ollama Service  │◄─┘            │
│  │  (Port 11434)    │               │
│  └──────────────────┘               │
│         ▲                           │
│         │ HTTP                      │
│         │ localhost:11434           │
│         │                           │
│  [Persisted Models Volume]          │
│                                     │
└─────────────────────────────────────┘
         │
         │ localhost:8501
         │
    [Your Browser]
```

## Clean Up

```bash
# Stop all containers
docker-compose down

# Remove images
docker rmi hr-policy-assistant ollama/ollama

# Remove all unused Docker resources
docker system prune -a

# Remove volumes (careful - deletes data!)
docker volume prune
```

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Verify Docker installation: `docker --version`
3. Test Docker setup: `docker run hello-world`
4. Check disk space: `docker system df`

---

**Last Updated**: February 2, 2026
**Version**: 1.0
