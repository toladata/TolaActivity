'''
converts all .shp in ./tmp/ to geojson and places it in data directory
Example command - ogr2ogr -f "GeoJSON" ../../AFG_adm2.json AFG_adm2.shp
'''
import os
from dircache import listdir

from gladmap.models import Boundary, Country, State
import django.db

cursor = django.db.connection.cursor()
import json

geo_data_dir = "/home/leon/projects/Pycharm/TolaActivity/gladmap/tmp/"
## {0} -> destination geojson {1} - source shape
cmd_template = 'ogr2ogr -f "GeoJSON" {0} {1}'

def run():
    print("Saving GeoJSON to DB")
    #process_shp()
    #save_geojson()
    split_geojson()


def split_geojson():
    for file in listdir(geo_data_dir):
        if file.endswith(".json"):
            f = file.replace(".json", "").replace("_adm", "")
            cname = f[0:3]
            level = int(f[3])
            #print(country, level)
            if cname == "DEU" and level == 2:
                with open(geo_data_dir + file) as jsonfile:
                    filecontent = jsonfile.read()
                    gj = json.loads(filecontent)
                    print cname, level
                    print gj["type"]

                    if level == 1:
                        State.objects.all().delete();

                    for feature in gj["features"]:
                        cname = feature["properties"]["ISO"]
                        clist = Country.objects.all().filter(code=cname)

                        if len(clist) == 0:
                            country = Country(code=cname, boundary=feature["geometry"]["coordinates"])
                            country.save()
                        else:
                            country = clist[0]

                        if level == 1:
                            state = State(country=country,
                                          code=feature["properties"]["HASC_1"],
                                          name=feature["properties"]["NAME_1"],
                                          boundary=feature["geometry"]["coordinates"]
                                          )
                            state.save()

                            print feature["properties"]["ISO"], feature["properties"]["NAME_1"], feature["properties"]["HASC_1"]
                            #print feature["properties"]["ISO"], feature["properties"]["NAME_2"], feature["properties"]["HASC_2"]
                            print len(feature["geometry"]["coordinates"])

                        if level == 2:
                            print feature["properties"]["ISO"], feature["properties"]["NAME_2"], feature["properties"]["HASC_2"]
                            print len(feature["geometry"]["coordinates"])


                        #for i in range(0, len(feature["geometry"]["coordinates"])):
                        #    print "  "+str(len(feature["geometry"]["coordinates"][i]))


def convert_shp_json(path_shp):
	path_geo_file = geo_data_dir + path_shp.split("/")[-1].split(".")[0] + ".json"
	command = cmd_template.format(path_geo_file,path_shp)
	print command
	os.system(command)

def process_shp():
	for file in listdir(geo_data_dir):
		if file.endswith(".shp"):
			convert_shp_json(geo_data_dir + file)

def save_geojson():
    for file in listdir(geo_data_dir):
        if file.endswith(".json"):
            f = file.replace(".json", "").replace("_adm", "")
            country = f[0:3]
            level = f[3]
            with open(geo_data_dir + file) as fc:
                s = fc.read()
                bd = Boundary(geo_json=s, country=country, level=level)
                #django.db.connection.close()
                bd.save()
                print country, level, s[0:10]


if __name__ == "__main__":
    for file in listdir(geo_data_dir):
        if file.endswith(".json"):
            f = file.replace(".json","").replace("_adm", "")
            country = f[0:3]
            level = f[3]
            print country, level




