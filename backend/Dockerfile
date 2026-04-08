# Use an official Python runtime as a parent image
# Using bookworm (non-slim) for better build tool compatibility
FROM python:3.11-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# CRITICAL: Set Cargo home to a writable directory BEFORE installing anything Rust-related
# Render build environment has a read-only /usr/local/cargo
ENV CARGO_HOME=/tmp/cargo
ENV PATH="/tmp/cargo/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust via rustup (more reliable than apt-get for maturin builds)
RUN mkdir -p $CARGO_HOME && chmod -R 777 $CARGO_HOME \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Install tiktoken explicitly first to catch errors early
RUN pip install --no-cache-dir tiktoken
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
