from rest_framework import serializers
from rest_framework.reverse import reverse

from formlibrary.models import (Distribution, CustomForm, Beneficiary,
                                CustomFormField, FieldType)
from indicators.models import (
    Indicator, IndicatorType, Level, Frequency, Objective, DisaggregationType,
    ExternalService, ExternalServiceRecord, StrategicObjective, PeriodicTarget,
    CollectedData, TolaTable, DisaggregationValue, DisaggregationLabel)
from workflow import models as wfm


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = wfm.User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_self')

    def get_self(self, obj):
        request = self.context['request']
        return reverse('group-detail', kwargs={'pk': obj.id}, request=request)

    class Meta:
        model = wfm.Group
        fields = '__all__'


class WorkflowLevel1Serializer(serializers.HyperlinkedModelSerializer):
    workflow_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()
    status = serializers.SerializerMethodField()
    budget = serializers.ReadOnlyField()
    actuals = serializers.ReadOnlyField()
    difference = serializers.SerializerMethodField()

    def get_status(self, obj):
        get_projects = wfm.WorkflowLevel2.objects.all().filter(
            workflowlevel1=obj)
        score = []
        red = ""
        yellow = ""
        green = ""

        for project_status in get_projects:
            if project_status.status == "red":
                score.append(red)
            if project_status.status == "yellow":
                score.append(yellow)
            if project_status.status == "green":
                score.append(green)
        if score:
            calculated_status = max(score)
        else:
            calculated_status = "green"

        return calculated_status

    def get_difference(self, obj):
        try:
            if obj.budget:
                return obj.budget - obj.actuals
            else:
                return 0
        except AttributeError:
            return None

    class Meta:
        model = wfm.WorkflowLevel1
        fields = '__all__'


class SectorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Sector
        fields = '__all__'


class ProjectTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.ProjectType
        fields = '__all__'


class OfficeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Office
        fields = '__all__'


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Budget
        fields = '__all__'


class SiteProfileSerializer(serializers.HyperlinkedModelSerializer):
    site_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.SiteProfile
        fields = '__all__'


class WorkflowLevel2Serializer(serializers.HyperlinkedModelSerializer):
    agreement_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.WorkflowLevel2
        fields = '__all__'


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Country
        fields = '__all__'


class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    indicator_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()
    actuals = serializers.ReadOnlyField()

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
    level = IndicatorLevelLightSerializer(read_only=True)
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
        fields = ('name', 'number', 'lop_target', 'indicator_type', 'level',
                  'sector', 'datacount')


class ProgramIndicatorSerializer(serializers.ModelSerializer):
    indicator_set = IndicatorLightSerializer(many=True, read_only=True)
    indicators_count = serializers.SerializerMethodField()

    def get_indicators_count(self, obj):
        return obj.indicator_set.count()

    class Meta:
        model = wfm.WorkflowLevel1
        fields = ('id', 'name', 'indicators_count', 'indicator_set')


class FrequencySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Frequency
        fields = '__all__'


class TolaUserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.TolaUser
        fields = '__all__'
        depth = 1


class IndicatorTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = IndicatorType
        fields = '__all__'


class ObjectiveSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Objective
        fields = '__all__'


class FundCodeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.FundCode
        fields = '__all__'


class DisaggregationTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    disaggregation_type = serializers.CharField(max_length=135)

    class Meta:
        model = DisaggregationType
        fields = '__all__'


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Level
        fields = '__all__'


class StakeholderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Stakeholder
        fields = '__all__'


class ExternalServiceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ExternalService
        fields = '__all__'


class ExternalServiceRecordSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ExternalServiceRecord
        fields = '__all__'


class StrategicObjectiveSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = StrategicObjective
        fields = '__all__'


class StakeholderTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.StakeholderType
        fields = '__all__'


class ProfileTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.ProfileType
        fields = '__all__'


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.AdminLevelOne
        fields = '__all__'


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.AdminLevelTwo
        fields = '__all__'


class AdminLevelThreeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.AdminLevelThree
        fields = '__all__'


class VillageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.AdminLevelFour
        fields = '__all__'


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Contact
        fields = '__all__'


class DocumentationSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Documentation
        fields = '__all__'


class PeriodicTargetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = PeriodicTarget
        fields = '__all__'


class CollectedDataSerializer(serializers.HyperlinkedModelSerializer):
    data_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = CollectedData
        fields = '__all__'


class TolaTableSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = TolaTable
        fields = '__all__'


class DisaggregationValueSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = DisaggregationValue
        fields = '__all__'


class DisaggregationLabelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = DisaggregationLabel
        fields = '__all__'


class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Checklist
        fields = '__all__'


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Organization
        fields = '__all__'


class WorkflowModulesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.WorkflowModules
        fields = '__all__'


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Currency
        fields = '__all__'


class ApprovalTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.ApprovalType
        fields = '__all__'


class ApprovalWorkflowSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.ApprovalWorkflow
        fields = '__all__'


class BeneficiarySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Beneficiary
        fields = '__all__'


class DistributionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Distribution
        fields = '__all__'


class RiskRegisterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.RiskRegister
        fields = '__all__'


class IssueRegisterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.IssueRegister
        fields = '__all__'


class CustomFormSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomForm
        fields = '__all__'


class CustomFormFieldSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = CustomFormField
        fields = '__all__'


class CodedFieldSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.CodedField
        fields = '__all__'


class CodedFieldValuesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.CodedFieldValues
        fields = '__all__'


class FieldTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = FieldType
        fields = '__all__'


class LandTypeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.LandType
        fields = '__all__'


class InternationalizationSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Internationalization
        fields = '__all__'


class TolaUserFilterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.TolaUserFilter
        fields = '__all__'


class StakeholderFullSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    country = CountrySerializer(read_only=True)
    contact = ContactSerializer(read_only=True, many=True)
    sectors = SectorSerializer(read_only=True, many=True)
    approval = ApprovalTypeSerializer(read_only=True, many=True)

    class Meta:
        model = wfm.Stakeholder
        fields = '__all__'


class WorkflowLevel2FullSerializer(serializers.HyperlinkedModelSerializer):
    agreement_key = serializers.UUIDField(read_only=True)
    id = serializers.ReadOnlyField()
    workflowlevel1 = WorkflowLevel1Serializer(read_only=True)
    project_type = ProjectTypeSerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    budget = BudgetSerializer(read_only=True)

    class Meta:
        model = wfm.WorkflowLevel2
        fields = '__all__'


class WorkflowLevel2SortSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.WorkflowLevel2Sort
        fields = '__all__'


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Award
        fields = '__all__'


class WorkflowTeamSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.WorkflowTeam
        fields = '__all__'


class MilestoneSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Milestone
        fields = '__all__'


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Portfolio
        fields = '__all__'


class DashboardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Dashboard
        fields = '__all__'


class WidgetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.Widget
        fields = '__all__'


class SectorRelatedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.SectorRelated
        fields = '__all__'


class WorkflowLevel1SectorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = wfm.WorkflowLevel1Sector
        fields = '__all__'
