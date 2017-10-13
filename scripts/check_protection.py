from workflow.models import *
import urllib
import os
import re

def run():
    print "Checking security status on models"
    try:
        check_status()
    except Exception, e:
        print(e.message)


def check_status():
    model_files = []
    for dir in os.listdir("./"):
        p = "./" + dir
        if os.path.exists(p) and os.path.isdir(p) and os.path.exists(p + "/models.py"):
            print dir
            with open(p + "/models.py", "r") as mf:
                fc = ""
                for l in mf.readlines():
                    fc = fc + l

                search = re.findall("class (.*)\((.*)\)", fc)

                if search is not None:
                    for res in search:
                        if res[1] is not "SecurityModel":
                            print "  "+res[0] + " " + res[1]
