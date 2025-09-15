# DB2 for i Docker Query Tool

A simple Docker-based tool for connecting to IBM DB2 for i (AS/400) and executing SQL queries.

## Quick Start

1. **Copy the environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` with your DB2 connection details:**
   ```bash
   DB2_HOST=your-db2-host.com
   DB2_PORT=50000
   DB2_DATABASE=your-database
   DB2_USERNAME=your-username
   DB2_PASSWORD=your-password
   ```

3. **Build and run:**
   ```bash
   docker build -t db2-query .
   docker run --env-file .env db2-query
   ```

## Usage Examples

### Basic Usage
```bash
# Run with default query (list schemas)
docker run --env-file .env db2-query

# Test connection
docker run --env-file .env db2-query python db2_query.py --test-connection

# Custom query
docker run --env-file .env db2-query python db2_query.py --query "SELECT * FROM MYTABLE FETCH FIRST 10 ROWS ONLY"

# Show connection info (password masked)
docker run --env-file .env db2-query python db2_query.py --show-connection
```

### Using Docker Compose
```bash
# Run with docker-compose
docker-compose run db2-query

# Custom query with docker-compose
docker-compose run db2-query python db2_query.py --query "SELECT CURRENT_TIMESTAMP FROM SYSIBM.SYSDUMMY1"
```

### Interactive Mode
```bash
# Run container interactively to execute multiple queries
docker run -it --env-file .env db2-query bash

# Then inside the container:
python db2_query.py --query "SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA='MYSCHEMA' FETCH FIRST 5 ROWS ONLY"
```

## Configuration

### Environment Variables
- `DB2_HOST` - DB2 server hostname/IP
- `DB2_PORT` - Port (usually 50000)
- `DB2_DATABASE` - Database name
- `DB2_USERNAME` - Username for authentication
- `DB2_PASSWORD` - Password for authentication
- `DB2_SCHEMA` - Default schema (optional)

### Command Line Options
- `--query, -q` - SQL query to execute
- `--test-connection, -t` - Test connection only
- `--show-connection, -c` - Show connection info

## Sample Queries

```sql
-- List all schemas
SELECT * FROM QSYS2.SYSCHEMAS FETCH FIRST 10 ROWS ONLY

-- List tables in a schema
SELECT * FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA='MYSCHEMA'

-- Get current timestamp
SELECT CURRENT_TIMESTAMP FROM SYSIBM.SYSDUMMY1

-- List active jobs
SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO()) FETCH FIRST 10 ROWS ONLY
```

## Project Structure
```
.
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
├── db2_query.py       # Main application script
├── .env.template      # Environment template
├── docker-compose.yml # Docker Compose configuration
└── README.md          # This file
```

## Notes
- Uses `ibm-db` Python driver for DB2 connectivity
- Supports both environment variables and .env files
- Minimalistic design focused on query execution
- Connection credentials are never displayed in logs (password masked)
- Built on Python 3.12 slim image for smaller footprint