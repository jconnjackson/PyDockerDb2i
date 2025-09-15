#!/usr/bin/env python3
import os
import sys
import pyodbc
import argparse
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


def get_connection_string():
    """Build ODBC connection string from environment variables"""
    host = os.getenv('DB2_HOST', '')
    port = os.getenv('DB2_PORT', '446')
    database = os.getenv('DB2_DATABASE', '')
    username = os.getenv('DB2_USERNAME', '')
    password = os.getenv('DB2_PASSWORD', '')

    # IBM i Access ODBC connection string - using exact driver path
    conn_str = f"DRIVER=/opt/ibm/iaccess/lib64/libcwbodbc.so;SYSTEM={host};PORT={port};DATABASE={database};UID={username};PWD={password};NAMING=1;TRANSLATE=1;"

    return conn_str


def execute_query(query, show_connection_info=False):
    """Execute a SQL query and display results"""
    try:
        conn_str = get_connection_string()

        if show_connection_info:
            # Show connection info (without password)
            safe_conn_str = conn_str.replace(f"PWD={os.getenv('DB2_PASSWORD', '')};", "PWD=***;")
            print(f"Connection string: {safe_conn_str}")
            print("-" * 50)

        print("Connecting to DB2 for i...")
        conn = pyodbc.connect(conn_str)

        print("✓ Connected successfully!")
        print(f"Executing query: {query}")
        print("-" * 50)

        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Print header
        print(" | ".join(f"{col:<15}" for col in columns))
        print("-" * (17 * len(columns)))

        # Fetch and display results
        row_count = 0
        for row in cursor:
            row_count += 1
            row_data = [str(value) if value is not None else "NULL" for value in row]
            print(" | ".join(f"{d:<15}" for d in row_data))

        if row_count == 0:
            print("No rows returned.")
        else:
            print(f"\n✓ Query completed. {row_count} row(s) returned.")

        # Close connections
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='DB2 for i Query Tool')
    parser.add_argument('--query', '-q', type=str,
                        default="SELECT * FROM QSYS2.SYSCHEMAS FETCH FIRST 5 ROWS ONLY",
                        help='SQL query to execute')
    parser.add_argument('--show-connection', '-c', action='store_true',
                        help='Show connection information')
    parser.add_argument('--test-connection', '-t', action='store_true',
                        help='Test connection only')

    args = parser.parse_args()

    print("=" * 60)
    print("DB2 for i Query Tool")
    print("=" * 60)

    # Test connection mode
    if args.test_connection:
        result = execute_query("SELECT CURRENT_TIMESTAMP FROM SYSIBM.SYSDUMMY1", args.show_connection)
        sys.exit(0 if result else 1)

    # Execute the specified query
    result = execute_query(args.query, args.show_connection)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()