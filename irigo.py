# coding:utf-8
import bonobo
import requests
import psycopg2
import env

# Les données de connexion à la base
relationnal_connection_data = {
    "dbname": env.dbname,
    "user": env.user,
    "password": env.password,
    "host": env.host,
    "port": env.port
}

# Fonction utilisant un générateur qui appelle l'url de l'API et retourne les résultats (records)
def fetch_desserte_data():
    url = "https://data.angers.fr/api/records/1.0/search/?dataset=bus-tram-topologie-dessertes&"
    response = requests.get(url)
    for record in response.json().get("records"):
        yield record

# Fonction utilisant un générateur qui retourne uniquement les champs intéressants parmi les données récupérées
def get_interesting_fields(record):
    result = {
        "line_id": record["fields"]["mnemoligne"],
        "stop_id": record["fields"]["idarret"],
        "line_name": record["fields"]["nomligne"],
        "stop_name": record["fields"]["nomarret"]
    }
    yield result

# Fonction utilisant un générateur qui se connecte à la base et tente d'enregistrer les données dans la table des lignes
def insert_in_relationnal(record):
    with psycopg2.connect(**relationnal_connection_data) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO line (id, name) VALUES (%s, %s);
                """, (record["line_id"], record["line_name"]))
            except psycopg2.IntegrityError as e:
                print("line already exists", record["line_id"])
    yield record

# Génération du Graph bonobo
graph = bonobo.Graph()
graph.add_chain(
    fetch_desserte_data, 
    get_interesting_fields,
    insert_in_relationnal,
    bonobo.PrettyPrinter()
)
graph.add_chain(graph, _input=fetch_desserte_data)
r = bonobo.run(graph)
