# PyDockerDb2i

___Python + Docker + DB2 for i___

Boilerplate code that for creating containerized applications using Python that must connect to DB2 for IBM System i

Supports running queries from the command line out of the box and can be used either for starting new projects or
as example code to show how these three technologies can be combined

## Quick Start

1. **Copy the environment template:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` with your DB2 connection details:**

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

### Using Docker Compose (after editing docker-compose.yml file)
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
python db2_query.py --query "SELECT TABLE_NAME FROM QSYS2.SYSTABLES WHERE TABLE_SCHEMA='QSYS2' FETCH FIRST 5 ROWS ONLY"
```

## Configuration

### Environment Variables
- `DB2_HOST` - DB2 server hostname/IP
- `DB2_PORT` - Port (usually 50000 or 446)
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
SELECT * FROM QSYS2.SYSSCHEMAS FETCH FIRST 10 ROWS ONLY

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
├── README.md          # This file
├── Dockerfile         # Container definition
├── requirements.txt   # Python dependencies
├── db2_query.py       # Main application script
├── .env.template      # Environment template
├── docker-compose.yml # Docker Compose configuration
├── odbc.ini           # Refers to odbcinst.ini to define the Data Source Names (DSNs)
├── odbcinst.ini       # Defines drivers available to Open DataBase Connectivity for System
└── ibm-iaccess-1.1.0.28-1.0.amd64 # From:
                       # https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/main/binary-amd64/
```