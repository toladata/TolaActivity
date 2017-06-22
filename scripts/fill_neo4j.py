from os import listdir
from os.path import isfile, join

from neo4j.v1 import GraphDatabase, basic_auth
import pickle, os, random, string


def generate_text(length):
    return "".join([random.choice(string.letters) for i in xrange(length)])

def create_countries():
    countries = ["Germany", "Afghanistan", "USA", "India", "Nigeria", "Brazil"]
    count = 0
    for c in countries:
        count = count + 1

        session.run(
            "MERGE (c:Country {name:{name}, id:{id}})",
            {
                "id": count,
                "name": c
            }
        )

def create_indicators(max=100):
    for i in range(0, max):
        session.run(
            "MERGE (i:Indicator {name:{name}, type:{type}, description:{description}, status:{status}})",
            {
                "id": i,
                "name": generate_text(random.randint(5,20)),
                "type": generate_text(random.randint(5,10)),
                "description": generate_text(random.randint(10,20)),
                "status": generate_text(random.randint(5,10))
            }
        )

def create_demo(max_projects):
    for i in range(0, max_projects):
        # Add workflow object

        session.run(
            "MERGE (w:Workflow {name:{name}, project_activity:{project_activity}, description:{description}, funding_status:{funding_status}})",
            {
                "id": i,
                "name": generate_text(random.randint(5,20)),
                "description": generate_text(random.randint(50,500)),
                "project_activity": generate_text(random.randint(10,20)),
                "funding_status": generate_text(random.randint(5,10))
            }
        )




"""
        country
                    gbdTx = "MATCH (c:Condition {title: {cond_title}}) " \
                            "MATCH (b:Burden) WHERE {icd10code} IN b.icd10codes " \
                            "CREATE UNIQUE (c)-[:HAS_BURDEN]->(b)"

        stakeholder

        Sector

        Indicator
"""
def create_relations():
    result = session.run("MATCH (w:Workflow) RETURN w.name as name, ID(w) as id")

    for record in result:
        print(record["name"], record["id"])

        session.run("MATCH (w:Workflow) WHERE ID(w) = {w_id} MATCH (c:Country) WHERE ID(c) = {c_id} CREATE UNIQUE (w)-[:LOCATED_IN]->(c)",
                             {"w_id": record["id"], "c_id": random.randint(0, 6)}
                    )
        for n in range(1,random.randint(1,5)):
            session.run(
                "MATCH (w:Workflow) WHERE ID(w) = {w_id} MATCH (i:Indicator) WHERE ID(i) = {i_id} CREATE (w)-[:USES]->(i)",
                {"w_id": record["id"], "i_id": random.randint(0, 100)}
                )

    """
    
    
    session.run(
    "MATCH (w:Workflow {id: {w_id}}), (c:Country {id:{c_id}}), (i:Indicator {id:{i_id}})" +
    "CREATE UNIQUE (w)-[:LOCATED_IN]->(c)" +
    "CREATE UNIQUE (w)-[:USES]->(i)",
    {"w_id": i, "c_id": random.randint(0, 100), "i_id": random.randint(0, 6)}
)"""

# establish db connection
driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", ""))
session = driver.session()

#create_countries()
#create_indicators(100)
create_demo(1000)
create_relations()
