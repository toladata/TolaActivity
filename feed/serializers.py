from rest_framework import serializers

from workflow.models import *
from indicators.models import *
from formlibrary.models import *
from django.contrib.auth.models import User
from rest_framework.serializers import ReadOnlyField


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class WorkflowLevel1Serializer(serializers.HyperlinkedModelSerializer):
    workflow_key = serializers.UUIDField(read_only=True)

    class Meta:
        model = WorkflowLevel1
        fields = '__all__'


class SectorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sector
        fields = '__all__'


class ProjectTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectType
        fields = '__all__'


class OfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Office
        fields = '__all__'


class SiteProfileSerializer(serializers.HyperlinkedModelSerializer):
    site_key = serializers.UUIDField(read_only=True)

    class Meta:
        model = SiteProfile
        fields = '__all__'


class WorkflowLevel2Serializer(serializers.HyperlinkedModelSerializer):
    agreement_key = serializers.UUIDField(read_only=True)

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    indicator_key = serializers.UUIDField(read_only=True)

    class Meta:
        model = Indicator
        fields = '__all__'


class IndicatorTypeLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorType
        fields = ('id', 'indicator_type')


class IndicatorLevelLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('id', 'name')


class IndicatorLightSerializer(serializers.ModelSerializer):
    sector = serializers.SerializerMethodField()
    indicator_type = IndicatorTypeLightSerializer(many=True, read_only=True)
    level = IndicatorLevelLightSerializer(many=True, read_only=True)
    datacount = serializers.SerializerMethodField()

    def get_datacount(self, obj):
        # Returns the number of collecteddata points by an indicator
        return obj.collecteddata_set.count()

    def get_sector(self, obj):
        if obj.sector is None:
            return ''
        return {"id": obj.sector.id, "name": obj.sector.sector}

    class Meta:
        model = Indicator
        fields = ('name', 'number', 'lop_target', 'indicator_type', 'level', 'sector', 'datacount')


class ProgramIndicatorSerializer(serializers.ModelSerializer):
    indicator_set = IndicatorLightSerializer(many=True, read_only=True)
    indicators_count = serializers.SerializerMethodField()

    def get_indicators_count(self, obj):
        return obj.indicator_set.count()

    class Meta:
        model = WorkflowLevel1
        fields = ('id', 'name', 'indicators_count', 'indicator_set')


class ReportingFrequencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ReportingFrequency
        fields = '__all__'


class TolaUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TolaUser
        fields = '__all__'


class IndicatorTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = IndicatorType
        fields = '__all__'


class ObjectiveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Objective
        fields = '__all__'


class FundCodeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FundCode
        fields = '__all__'


class DisaggregationTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DisaggregationType
        fields = '__all__'


class LevelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Level
        fields = '__all__'


class StakeholderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Stakeholder
        fields = '__all__'


class ExternalServiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExternalService
        fields = '__all__'


class ExternalServiceRecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExternalServiceRecord
        fields = '__all__'


class StrategicObjectiveSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StrategicObjective
        fields = '__all__'


class StakeholderTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = StakeholderType
        fields = '__all__'


class ProfileTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileType
        fields = '__all__'


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = District
        fields = '__all__'


class AdminLevelThreeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdminLevelThree
        fields = '__all__'


class VillageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Village
        fields = '__all__'


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class DocumentationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Documentation
        fields = '__all__'


class CollectedDataSerializer(serializers.HyperlinkedModelSerializer):
    data_key = serializers.UUIDField(read_only=True)

    class Meta:
        model = CollectedData
        fields = '__all__'


class TolaTableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TolaTable
        # HyperlinkedModelSerializer does not include id field by default so manually setting it
        fields = ('id', 'name', 'table_id', 'owner', 'remote_owner', 'country', 'url', 'unique_count', 'create_date', 'edit_date')
        #fields = '__all__'


class DisaggregationValueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DisaggregationValue
        fields = '__all__'


class DisaggregationLabelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DisaggregationLabel
        fields = '__all__'


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class WorkflowModulesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkflowModules
        fields = '__all__'


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ApprovalTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApprovalType
        fields = '__all__'


class ApprovalWorkflowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'


class BeneficiarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'


class DistributionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Distribution
        fields = '__all__'


class CustomFormSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomForm
        fields = '__all__'


class CustomFormFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomFormField
        fields = '__all__'


class FieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FieldType
        fields = '__all__'
