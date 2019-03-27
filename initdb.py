# coding:utf-8
import psycopg2
import env

# Ce fichier sert à initialiser la base de données

# Les données de connexion à la base
relationnal_connection_data = {
    "dbname": env.dbname,
    "user": env.user,
    "password": env.password,
    "host": env.host,
    "port": env.port
}

# On se connecte à la base et on récupère un curseur (pour executer des instructions)
with psycopg2.connect(**relationnal_connection_data) as connection:
    # Si les tables line et stop existent, on les delete (clear database pour insertion de nouvelles données)
    with connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS line CASCADE
        """)
        cursor.execute("""
            DROP TABLE IF EXISTS stop CASCADE
        """)
    
    # Création de la table line qui va stocker les lignes de transports et stop qui va stocker les arrêts
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
        
        # On print dans la console les tables existantes pour vérifier qu'elles ont bien été insérées
        cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
        rows = cursor.fetchall()
        print("tables", "line" in [r[1] for r in rows])
