from .serializers import *
from workflow.models import *
from indicators.models import *
from formlibrary.models import *

from django.db.models import Count, Sum
from django.contrib.auth.models import User
from tola.util import getCountry
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from workflow.mixins import APIDefaultsMixin


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProgramIndicatorReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgramIndicatorSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = WorkflowLevel1.objects.prefetch_related('indicator_set', \
            'indicator_set__indicator_type',\
            'indicator_set__sector', 'indicator_set__level', \
            'indicator_set__collecteddata_set').all()
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WorkflowLevel1ViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    search by country name and workflowlevel1 name
    limit to users logged in country permissions
    """

    # Remove CSRF request verification for posts to this API
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WorkflowLevel1ViewSet, self).dispatch(*args, **kwargs)

    def list(self, request):
        user_countries = getCountry(request.user)
        if request.user.is_superuser:
            queryset = WorkflowLevel1.objects.all()
        else:
            queryset = WorkflowLevel1.objects.all().filter(country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    ordering_fields = ('country__country', 'name')
    filter_fields = ('country__country','name','level1_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = WorkflowLevel1.objects.all()
    serializer_class = WorkflowLevel1Serializer


class SectorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def __get__(self, instance, owner):
        if self.request.user.is_superuser:
            queryset = Sector.objects.all()
        else:
            user_org = TolaUser.objects.get(user=self.request.user).organization
            queryset = Sector.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = ProjectType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = ProjectType.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    def list(self, request):
        user_countries = getCountry(request.user)
        if request.user.is_superuser:
            queryset = Office.objects.all()
        else:
            queryset = Office.objects.all().filter(country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('country__country','country__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class SiteProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by country name and program name
    limit to users logged in country permissions
    """
    def list(self, request):
        user_countries = getCountry(request.user)
        if request.user.is_superuser:
            queryset = SiteProfile.objects.all()
        else:
            queryset = SiteProfile.objects.all().filter(country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = SiteProfile .objects.all()
    serializer_class = SiteProfileSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = Country.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Country.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class IndicatorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by country name and program name
    limit to users logged in country permissions
    """
    def list(self, request):
        if request.user.is_superuser:
            queryset = Indicator.objects.all()
        else:
            user_countries = getCountry(request.user)
            queryset = Indicator.objects.all().filter(workflowlevel1__country__in=user_countries).annotate(actuals=Sum('collecteddata__achieved'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Indicator.objects.annotate(actuals=Sum('collecteddata__achieved'))

    filter_fields = ('workflowlevel1__country__country','workflowlevel1__name','indicator_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class ReportingFrequencyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = ReportingFrequency.objects.all()
    serializer_class = ReportingFrequencySerializer


class TolaUserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving TolaUsers.

    """
    def list(self, request):
        queryset = TolaUser.objects.all()
        serializer = TolaUserSerializer(instance=queryset,context={'request': request},many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TolaUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TolaUserSerializer(instance=user, context={'request': request})
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = TolaUser.objects.all()
    serializer_class = TolaUserSerializer


class IndicatorTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = IndicatorType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = IndicatorType.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = IndicatorType.objects.all()
    serializer_class = IndicatorTypeSerializer


class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = Objective.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Objective.objects.all().filter(workflowlevel1__country__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class FundCodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = FundCode.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = FundCode.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = FundCode.objects.all()
    serializer_class = FundCodeSerializer


class DisaggregationTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = DisaggregationType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = DisaggregationType.objects.all().filter(country__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('country__organization__id','country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = DisaggregationType.objects.all()
    serializer_class = DisaggregationTypeSerializer


class LevelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = Level.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Level.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id','country__country','workflowlevel1__name')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class StakeholderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by Country
    Limited to logged in users accessible countires
    """
    def list(self, request):
        user_countries = getCountry(request.user)
        queryset = Stakeholder.objects.all().filter(country__in=user_countries)

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = StakeholderFullSerializer

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = StakeholderFullSerializer

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    filter_fields = ('country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Stakeholder.objects.all()
    serializer_class = StakeholderSerializer


class ExternalServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = ExternalService.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = ExternalService.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = ExternalService.objects.all()
    serializer_class = ExternalServiceSerializer


class ExternalServiceRecordViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = ExternalServiceRecord.objects.all()
    serializer_class = ExternalServiceRecordSerializer


class StrategicObjectiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = StrategicObjective.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = StrategicObjective.objects.all().filter(country__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('country__organization__id','country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = StrategicObjective.objects.all()
    serializer_class = StrategicObjectiveSerializer


class StakeholderTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = StakeholderType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = StakeholderType.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = StakeholderType.objects.all()
    serializer_class = StakeholderTypeSerializer


class ProfileTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = ProfileType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = ProfileType.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = ProfileType.objects.all()
    serializer_class = ProfileTypeSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class AdminLevelThreeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AdminLevelThree.objects.all()
    serializer_class = AdminLevelThreeSerializer


class VillageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Village.objects.all()
    serializer_class = VillageSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = Contact.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Contact.objects.all().filter(stakeholder__country__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('name','stakeholder__country__organization__id','stakeholder')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class DocumentationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        if request.user.is_superuser:
            queryset = Documentation.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Documentation.objects.all().filter(workflowlevel2__workflowlevel1__country__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__country__country','workflowlevel2__workflowlevel1__country__country','workflowlevel2__workflowlevel1__country__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer


class PeriodicTargetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = PeriodicTarget.objects.all()
    serializer_class = PeriodicTargetSerializer


class CollectedDataViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        user_countries = getCountry(request.user)
        queryset = CollectedData.objects.all().filter(workflowlevel1__country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('indicator__workflowlevel1__country__country', 'indicator__workflowlevel1__name','indicator','indicator__workflowlevel1__country__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = CollectedData.objects.all()
    serializer_class = CollectedDataSerializer
    pagination_class = SmallResultsSetPagination


class TolaTableViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        #user_countries = getCountry(request.user)
        #queryset = TolaTable.objects.all().filter(country__in=user_countries)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_countries = getCountry(self.request.user)
        queryset = TolaTable.objects.filter(country__in=user_countries)
        table_id = self.request.query_params.get('table_id', None)
        if table_id is not None:
            queryset = queryset.filter(table_id=table_id)
        return queryset

    filter_fields = ('table_id', 'country__country', 'collecteddata__indicator__workflowlevel1__name','country__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = TolaTableSerializer
    pagination_class = StandardResultsSetPagination
    queryset = TolaTable.objects.all()


class DisaggregationValueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        user_countries = getCountry(request.user)
        queryset = DisaggregationValue.objects.all().filter(disaggregation_label__disaggregation_type__country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('disaggregation_label__disaggregation_type__country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = DisaggregationValue.objects.all()
    serializer_class = DisaggregationValueSerializer
    pagination_class = StandardResultsSetPagination


class DisaggregationLabelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        queryset = DisaggregationLabel.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = DisaggregationLabel.objects.all()
    serializer_class = DisaggregationLabelSerializer
    pagination_class = StandardResultsSetPagination


class ChecklistViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__name','workflowlevel1__country__organization__id','workflowlevel1__country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    filter_fields = ('id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class WorkflowLevel2ViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by country name and program name
    limit to users logged in country permissions
    """
    # Remove CSRF request verification for posts to this API
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(WorkflowLevel2ViewSet, self).dispatch(*args, **kwargs)

    def list(self, request):
        user_countries = getCountry(request.user)
        queryset = WorkflowLevel2.objects.all().filter(workflowlevel1__country__in=user_countries)

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = WorkflowLevel2FullSerializer

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = WorkflowLevel2FullSerializer

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    """
    def post(self,request):

        for each agreement
            insert int and string fields direct
            if FK field

        return blank
    """

    filter_fields = ('workflowlevel1__country__country','workflowlevel1__name','level2_uuid','workflowlevel1__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = WorkflowLevel2.objects.all()
    serializer_class = WorkflowLevel2Serializer
    pagination_class = SmallResultsSetPagination


class WorkflowModulesViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = WorkflowModules.objects.all()
    serializer_class = WorkflowModulesSerializer


class WorkflowLevel2SortViewSet(viewsets.ModelViewSet):
    queryset = WorkflowLevel2Sort.objects.all()
    serializer_class = WorkflowLevel2SortSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ApprovalTypeViewSet(viewsets.ModelViewSet):
    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = ApprovalType.objects.all()
    serializer_class = ApprovalTypeSerializer


class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer


class BeneficiaryViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer


class DistributionViewSet(viewsets.ModelViewSet):
    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class CustomFormViewSet(viewsets.ModelViewSet):
    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = CustomForm.objects.all()
    serializer_class = CustomFormSerializer


class CustomFormFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomFormField.objects.all()
    serializer_class = CustomFormFieldSerializer


class FieldTypeViewSet(viewsets.ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class RiskRegisterViewSet(viewsets.ModelViewSet):
    queryset = RiskRegister.objects.all()
    serializer_class = RiskRegisterSerializer


class CodedFieldViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = CodedField.objects.all()
    serializer_class = CodedFieldSerializer


class CodedFieldValuesViewSet(viewsets.ModelViewSet):
    queryset = CodedFieldValues.objects.all()
    serializer_class = CodedFieldValuesSerializer


class IssueRegisterViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__country__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = IssueRegister.objects.all()
    serializer_class = IssueRegisterSerializer


class LandTypeViewSet(viewsets.ModelViewSet):
    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer


class InternationalizationViewSet(viewsets.ModelViewSet):

    queryset = Internationalization.objects.all()
    serializer_class = InternationalizationSerializer


class TolaUserFilterViewSet(viewsets.ModelViewSet):
    queryset = TolaUserFilter.objects.all()
    serializer_class = TolaUserFilterSerializer


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class WorkflowTeamViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTeam.objects.all()
    serializer_class = WorkflowTeamSerializer