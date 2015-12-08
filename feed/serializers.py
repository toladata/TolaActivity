from django.forms import widgets
from rest_framework import serializers
from activitydb.models import Program, Sector, ProjectType, Office, SiteProfile, Country, ProjectComplete, ProjectAgreement, ProjectTypeOther
from indicators.models import Indicator, ReportingFrequency, TolaUser, IndicatorType, Objective, DisaggregationType, Level
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ProgramSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Program


class SectorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sector


class ProjectTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectType


class OfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Office


class SiteProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SiteProfile


class CompleteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectComplete


class AgreementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectAgreement


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country


class ProjectTypeOtherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectTypeOther

class IndicatorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Indicator

class ReportingFrequencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReportingFrequency

class TolaUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TolaUser

class IndicatorTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IndicatorType

class ObjectiveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Objective


class DisaggregationTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DisaggregationType

class LevelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Level