# Use Python 3.11 slim image for smaller size and security
FROM python:3.11-slim

# Set the maintainer and metadata information
LABEL maintainer="oreakinodidi@microsoft.com"
LABEL description="Finance Tracker Backend API"

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Install system dependencies required for Python packages
# gcc: For compiling Python packages with C extensions
# postgresql-dev: For psycopg2 (PostgreSQL adapter)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first to leverage Docker layer caching
# This means if requirements don't change, Docker reuses this layer
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories for logs and set permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user for security
USER appuser

# Expose the port Flask runs on
EXPOSE 5000

# Health check to ensure the service is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Command to run the application with Gunicorn for production
# Using 4 workers and binding to all interfaces for Docker
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]