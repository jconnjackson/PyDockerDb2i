#!/usr/bin/env python3
import os
import sys
import ibm_db
import argparse
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


def get_connection_string():
    """Build DB2 connection string from environment variables"""
    host = os.getenv('DB2_HOST', 'localhost')
    port = os.getenv('DB2_PORT', '50000')
    database = os.getenv('DB2_DATABASE', 'SAMPLE')
    username = os.getenv('DB2_USERNAME', '')
    password = os.getenv('DB2_PASSWORD', '')

    conn_str = f"DATABASE={database};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"

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
        conn = ibm_db.connect(conn_str, "", "")

        if not conn:
            print("ERROR: Unable to connect to database")
            print(ibm_db.conn_errormsg())
            return False

        print("✓ Connected successfully!")
        print(f"Executing query: {query}")
        print("-" * 50)

        # Prepare and execute the statement
        stmt = ibm_db.exec_immediate(conn, query)

        if not stmt:
            print("ERROR: Unable to execute query")
            print(ibm_db.stmt_errormsg())
            return False

        # Fetch and display results
        row_count = 0
        while ibm_db.fetch_row(stmt):
            row_count += 1
            row_data = []
            col_count = ibm_db.num_fields(stmt)

            # Print header on first row
            if row_count == 1:
                headers = []
                for i in range(col_count):
                    field_name = ibm_db.field_name(stmt, i)
                    headers.append(field_name)
                print(" | ".join(f"{h:<15}" for h in headers))
                print("-" * (17 * col_count))

            # Print row data
            for i in range(col_count):
                value = ibm_db.result(stmt, i)
                row_data.append(str(value) if value is not None else "NULL")

            print(" | ".join(f"{d:<15}" for d in row_data))

        if row_count == 0:
            print("No rows returned.")
        else:
            print(f"\n✓ Query completed. {row_count} row(s) returned.")

        # Close connections
        ibm_db.close(conn)
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