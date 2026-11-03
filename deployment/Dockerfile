# Stage 1: Build Golang High-Performance Music Engine
FROM golang:1.22-alpine AS go-builder
WORKDIR /build
COPY golang/ .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o music-engine cmd/engine/main.go

# Stage 2: Runtime Container (Python 3.11 + Go Engine + FFmpeg)
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies including FFmpeg for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy Go binary from Stage 1
COPY --from=go-builder /build/music-engine /usr/local/bin/music-engine

# Copy Python requirements & application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "main.py"]

