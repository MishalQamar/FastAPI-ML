# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory to project root (where pyproject.toml and the `app` package live)
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (includes uvicorn from pyproject.toml)
RUN uv sync --frozen --no-dev

# Copy application code into the image
COPY . .

# Expose port 8000 (default FastAPI port)
EXPOSE 8000

# Run the FastAPI application from the project root so `app` is importable
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
