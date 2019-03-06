

class Geo():
    """
    
    """
    def in_boundary(self, point, geo_boundary):
        i=0
        for feature in geo_boundary["features"]:
            #if i > 0: continue
            i += 1
            print feature["properties"]
            #print feature["geometry"]
            print feature["geometry"]["type"]
            for coords in feature["geometry"]["coordinates"]:
                return self.in_coords(point, coords)
                #for geo_coord in coords:
                #    print(geo_coord[0],geo_coord[1])


    def in_coords(self, point, corners):
        result = False
        n = len(corners)
        if (n == 0
            or len(corners[0]) == 0
            or corners[0][0] is None
            or corners[0][1] is None
            or type(corners[0][0]) == list):
                return False
        #print type(corners[0][0])
        #if type(corners[0][0]) == list:
        #    print corners[0][0]

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
