# Multi-stage build for HR Policy Assistant

# Stage 1: Base image with Python
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Stage 2: Install dependencies
FROM base as builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-warn-script-location -r requirements.txt

# Stage 3: Final image
FROM base

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set PATH to include user's local bin
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY data/ /app/data/
COPY config/ /app/config/

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit application
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
