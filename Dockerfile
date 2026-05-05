# --- Stage 1: Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies into a local folder
COPY app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Stage 2: Final Runtime Stage ---
FROM python:3.11-slim

# Create a non-root user for security
RUN groupadd -g 1001 appuser && \
    useradd -r -u 1001 -g appuser appuser

WORKDIR /app

# Copy only the necessary files from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ .

# Ensure the app can write logs to a volume
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Set environment paths and switch to non-root user
ENV PATH=/home/appuser/.local/bin:$PATH
USER 1001

#  port is injected via docker-compose
EXPOSE 3000

CMD ["python", "main.py"]
