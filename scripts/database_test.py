import sys
import time

from workflow.models import WorkflowLevel1


def run():
    print("Starting Database test")
    n = 1000
    size = 0
    t1 = time.time()

    for i in range(0,n):
        result = simple_query()
        #result = relation_query()
        size = size + sys.getsizeof(result)

    t2 = time.time()

    print("Executed %d queries in %4.2fs time receiving %8.4f KiloBytes of data" % (n, (t2-t1), size/1024))


def simple_query():
    objects = WorkflowLevel1.objects.all()
    #for o in objects:
    #    print o.id
    return objects