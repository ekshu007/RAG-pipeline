from neo4j import GraphDatabase


URI =  "neo4j://127.0.0.1:7687"

USERNAME = "neo4j"

PASSWORD = "graphdb123"


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def get_driver():
    return driver