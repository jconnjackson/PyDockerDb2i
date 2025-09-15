# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies needed for DB2 connectivity
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make the script executable
RUN chmod +x db2_query.py

# Set default environment variables (can be overridden)
ENV DB2_HOST=your-db2-host
ENV DB2_PORT=50000
ENV DB2_DATABASE=your-database
ENV DB2_USERNAME=your-username
ENV DB2_PASSWORD=your-password
ENV DB2_SCHEMA=your-schema

# Default command
CMD ["python", "db2_query.py"]