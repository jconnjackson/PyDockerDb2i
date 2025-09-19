# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies needed for ODBC connectivity
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc \
    unixodbc-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the IBM i Access ODBC driver package
# From: https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/main/binary-amd64/
COPY ibm-iaccess-1.1.0.28-1.0.amd64.deb /tmp/

# Install IBM i Access ODBC driver
# See also: https://ibmi-oss-docs.readthedocs.io/en/latest/odbc/installation.html#linux
RUN dpkg -i /tmp/ibm-iaccess-1.1.0.28-1.0.amd64.deb || true && \
    apt-get update && \
    apt-get -f install -y && \
    rm /tmp/ibm-iaccess-1.1.0.28-1.0.amd64.deb

# Copy ODBC configuration files
COPY odbcinst.ini /etc/odbcinst.ini
COPY odbc.ini /etc/odbc.ini

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
ENV DB2_PORT=446
ENV DB2_DATABASE=your-database
ENV DB2_USERNAME=your-username
ENV DB2_PASSWORD=your-password
ENV DB2_SCHEMA=your-schema

# Default command
CMD ["python", "db2_query.py"]