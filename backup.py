import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error
from sh import pg_dump


# Load environment variables from .env file
load_dotenv()

try:
    # Get connection parameters from environment variables
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    master_database = os.getenv('MASTER_DB')
    backup_dir = os.getenv('BACKUP_DIR')
    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        # Connect to 'postgres' database to list all databases
        database=master_database
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Execute query to list all databases
    cursor.execute(
        "SELECT datname FROM pg_database WHERE datistemplate = false")

    # Fetch all database names
    databases = cursor.fetchall()

    print("Backup database..:")
    for db in databases:
        db_name = db[0]
        print(f"- {db_name}")
        try:
            pg_dump(f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}" ,_out=f"{backup_dir}/{db_name}.sql")
            print(f"{db_name} backup successful")
        except ErrorReturnCode_2:
            print(f"Unable to backup database {db_name}")
        except ErrorReturnCode:
            print(f"Unknown error backing up database {db_name}")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL:", error)

finally:
    # Close database connection
    if 'connection' in locals():
        cursor.close()
        connection.close()
        print("\nDatabase connection closed.")
