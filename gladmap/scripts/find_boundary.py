"""
converts all .shp in ./tmp/ to geojson and places it in data directory
Example command - ogr2ogr -f "GeoJSON" ../../AFG_adm2.json AFG_adm2.shp
"""
import django.db
from gladmap.models import Boundary

cursor = django.db.connection.cursor()
geo_data_dir = "/home/leon/projects/Pycharm/TolaActivity/gladmap/tmp/"
## {0} -> destination geojson {1} - source shape
cmd_template = 'ogr2ogr -f "GeoJSON" {0} {1}'

def run():
    print("Finding Boundary test")
    country = "SSD"
    gadm = Boundary.objects.all().filter(country=country)
    print gadm.count()
    #print type(gadm[0].geo_json)
    gj = gadm[0].geo_json
    #print(gj)
    i = 0
    for feature in gj["features"]:
        if i > 0: continue
        i += 1
        print feature["properties"]
        #print feature["geometry"]
        print feature["geometry"]["type"]
        for coords in feature["geometry"]["coordinates"]:
            print len(coords)
            print in_coords((32.0622291564942, 5.211561203002987), coords)
            #for geo_coord in coords:
            #    print(geo_coord[0],geo_coord[1])

def in_coords(point, corners):
    result = False
    n = len(corners)
    p1x = float(corners[0][0])
    p1y = float(corners[0][1])
    for i in range(n + 1):
        p2x = float(corners[i % n][0])
        p2y = float(corners[i % n][1])
        if point[1] > min(p1y, p2y):
            if point[0] <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or point[0] <= xinters:
                    result = not result
        p1x, p1y = p2x, p2y
    return result


