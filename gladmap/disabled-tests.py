from django.test import TestCase
from gladmap.models import Boundary
from gladmap.geo import Geo
# Create your tests here.


class GladmapTests(TestCase):
    fixtures = ['single-boundary']

    def testFixtureIsLoaded(self):
        b = Boundary.objects.all()
        self.assertEqual(len(b), 1)
