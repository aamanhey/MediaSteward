# Stage 1: Install dependencies (cached stage)
FROM python:3.10 AS builder

# Set working directory
WORKDIR /app

# Install system dependencies (for Tesseract, OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final runtime environment
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy necessary system tools (e.g., Tesseract) from the previous stage
COPY --from=builder /usr/bin/tesseract /usr/bin/tesseract
COPY --from=builder /usr/lib /usr/lib

# Copy installed Python libraries from builder
COPY --from=builder /usr/local /usr/local

# Copy the project files
COPY . .

# Set entrypoint
CMD ["python", "main.py"]
