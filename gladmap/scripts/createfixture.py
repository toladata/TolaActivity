from django.core import serializers
from gladmap.models import Boundary

def run():
    data = serializers.serialize("json", Boundary.objects.all().filter(id=1))

    out = open("gladmap/fixtures/single-boundary.json", "w")
    out.write(data)
    out.close()
