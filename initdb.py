import psycopg2
import env

relationnal_connection_data = {
    "dbname": env.dbname,
    "user": env.user,
    "password": env.password,
    "host": env.host,
    "port": env.port
}

with psycopg2.connect(**relationnal_connection_data) as connection:
    with connection.cursor() as cursor:
        cursor.execute("""
        DROP TABLE IF EXISTS line CASCADE
        """)
        cursor.execute("""
        DROP TABLE IF EXISTS stop CASCADE
        """)
    
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS line (
            id VARCHAR(256) PRIMARY KEY,
            name VARCHAR(256)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stop (
            id VARCHAR(256) PRIMARY KEY,
            name VARCHAR(256),
            line_id VARCHAR(256) REFERENCES line (id),
            lon REAL,
            lat REAL
        );
        """)

        cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
        rows = cursor.fetchall()
        print("tables", "line" in [r[1] for r in rows])
