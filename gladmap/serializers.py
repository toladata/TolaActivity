from rest_framework import serializers
from models import Boundary, Country, State


class BoundarySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Boundary
        fields = '__all__'


class BoundaryListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Boundary
        fields = ('url','country','level')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CountryListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('url','code')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class StateListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'code', 'country', 'url')

