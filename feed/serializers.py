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
        fields=(
                'program',
                'date_of_request',
                'project_name',
                'project_type',
                'project_activity',
                'project_description',
                'site',
                'activity_code',
                'office',
                'sector',
                'project_design',
                'account_code',
                'lin_code',
                'stakeholder',
                'effect_or_impact',
                'expected_start_date',
                'expected_end_date',
                'expected_duration',
                'total_estimated_budget',
                'mc_estimated_budget',
                'local_total_estimated_budget',
                'local_mc_estimated_budget',
                'exchange_rate',
                'exchange_rate_date',
                'estimation_date',
                'estimated_by',
                'estimated_by_date',
                'checked_by',
                'checked_by_date',
                'reviewed_by',
                'reviewed_by_date',
                'finance_reviewed_by',
                'finance_reviewed_by_date',
                'me_reviewed_by',
                'me_reviewed_by_date',
                'capacity',
                'evaluate',
                'approval',
                'approved_by',
                'approved_by_date',
                'approval_submitted_by',
                'approval_remarks',
                'justification_background',
                'risks_assumptions',
                'justification_description_community_selection',
                'description_of_project_activities',
                'description_of_government_involvement',
                'description_of_community_involvement',
                'community_project_description')


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
        fields = ('url', 'name','country', 'countries')

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