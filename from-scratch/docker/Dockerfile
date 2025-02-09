# Stage 1: Builder
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.10-slim
WORKDIR /app
# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY . .

# Expose a port for monitoring endpoints (e.g., health checks)
EXPOSE 8000

# Health check for container
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD curl -f http://localhost:8000/health || exit 1

# Set the entry point to execute the main script
CMD ["python", "main.py"]
