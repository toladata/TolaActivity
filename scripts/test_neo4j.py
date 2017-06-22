from neo4j.v1 import GraphDatabase, basic_auth
import time, sys

driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=basic_auth("neo4j", ""))
session = driver.session()


def simple_query():
    res = session.run("MATCH (w:Workflow) RETURN * LIMIT 2000") # w.name as name, ID(w) as id

    #for record in res:
        #print(record["id"])

    return res


def relation_query():
    return session.run('MATCH (w:Workflow)-[r:USES]->(i:Indicator), (w)-[l:LOCATED_IN]->(c1:Country {name:"Afghanistan"}) RETURN *')

n = 1000
size = 0
t1 = time.time()

for i in range(0,n):
    result = simple_query()
    #result = relation_query()
    size = size + sys.getsizeof(result)

t2 = time.time()

print("Executed %d queries in %4.2fs time receiving %8.4f KiloBytes of data" % (n, (t2-t1), size/1024))
