from rest_framework import serializers

from formlibrary.models import BinaryField


class BinaryFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinaryField
        fields = ('id', 'name')


class BinaryFieldImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BinaryField
        fields = '__all__'

