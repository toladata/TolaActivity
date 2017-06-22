from django.test import TestCase
from gladmap.models import Boundary
from gladmap.geo import Geo
# Create your tests here.


class GladmapTests(TestCase):
    fixtures = ['single-boundary']

    def testFixtureIsLoaded(self):
        b = Boundary.objects.all()
        self.assertEqual(len(b), 1)

    def testLocationMarker(self):
        """
        Tests the location marker functionality.
        :return: 
        """
        gadm = Boundary.objects.all().filter(country="CAF")
        gj = gadm[0].geo_json
        point = (22.22046279807357, 8.74786376953125)
        geo = Geo()
        dist = geo.find_district(point, gj)
        self.assertEqual(dist["NAME_2"], "Djemah")

    def testLocationMarkerNegative(self):
        """
        Test case testing location marker with a location in Iraq in CAF
        should return false
        :return: 
        """
        gadm = Boundary.objects.all().filter(country="CAF")
        gj = gadm[0].geo_json
        point = (33.1373748779298, 44.22711944580078)
        geo = Geo()
        dist = geo.find_district(point, gj)
        self.assertEqual(dist, False)
