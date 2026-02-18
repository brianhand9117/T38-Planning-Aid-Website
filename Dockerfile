# Multi-stage Dockerfile for T-38 Planning Aid Email Service
# Supports both web server and worker modes

# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Create app user (security best practice)
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to appuser
USER appuser

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Expose port (only used by web service)
EXPOSE 5000

# Default to web mode, can be overridden in docker-compose
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "run:app"]
