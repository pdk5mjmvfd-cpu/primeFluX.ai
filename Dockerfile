# Multi-stage Docker build for ApopToSiS v3
# Supports ARM64 (Pi/Jetson) and x86_64 with optional GPU

ARG ARCH=amd64
ARG PYTHON_VERSION=3.11

# Builder stage
FROM python:${PYTHON_VERSION}-slim-bullseye AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh || echo "Ollama install skipped"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:${PYTHON_VERSION}-slim-bullseye

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PRESENCE_OP=1
ENV APOP_MODE=local
ENV QUANTA_PATH=/app/experience/ledger.jsonl

# Expose ports
EXPOSE 8000 8501

# Default command
CMD ["python", "-m", "uvicorn", "api.fastapi_interface:app", "--host", "0.0.0.0", "--port", "8000"]
