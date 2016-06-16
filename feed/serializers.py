from rest_framework import serializers
from activitydb.models import Program, Sector, ProjectType, Office, SiteProfile, Country, ProjectComplete, \
    ProjectAgreement, CustomDashboard, Stakeholder, Capacity, Evaluate, ProfileType, \
    Province, District, AdminLevelThree, Village, StakeholderType, Contact, Documentation
from indicators.models import Indicator, ReportingFrequency, TolaUser, IndicatorType, Objective, DisaggregationType, \
    Level, ExternalService, ExternalServiceRecord, StrategicObjective, CollectedData, TolaTable, DisaggregationValue
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


class StakeholderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stakeholder


class CustomDashboardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CustomDashboard


class ExternalServiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExternalService


class ExternalServiceRecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExternalServiceRecord


class StrategicObjectiveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StrategicObjective


class StakeholderTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StakeholderType


class CapacitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Capacity


class EvaluateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Evaluate


class ProfileTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileType


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Province


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = District


class AdminLevelThreeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdminLevelThree


class VillageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Village


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact


class DocumentationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Documentation


class CollectedDataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CollectedData


class TolaTableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TolaTable


class DisaggregationValueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DisaggregationValue