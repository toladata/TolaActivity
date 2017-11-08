from django.db.models import Count, Sum
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .serializers import *
from workflow.models import *
from indicators.models import *
from formlibrary.models import *
from .permissions import *
from tola.util import getCountry, getLevel1


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
        queryset = WorkflowLevel1.objects.prefetch_related(
            'indicator_set',
            'indicator_set__indicator_type',
            'indicator_set__sector', 'indicator_set__level',
            'indicator_set__collecteddata_set').all()
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
        if request.user.is_superuser:
            queryset = WorkflowLevel1.objects.all().annotate(
                budget=Sum('workflowlevel2__total_estimated_budget'),
                actuals=Sum('workflowlevel2__actual_cost'))
        elif ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list(
                'name', flat=True):
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = WorkflowLevel1.objects.all().filter(
                organization=user_org).annotate(
                budget=Sum('workflowlevel2__total_estimated_budget'),
                actuals=Sum('workflowlevel2__actual_cost'))
        else:
            user_level1 = getLevel1(request.user)
            queryset = WorkflowLevel1.objects.all().filter(
                id__in=user_level1).annotate(
                budget=Sum('workflowlevel2__total_estimated_budget'),
                actuals=Sum('workflowlevel2__actual_cost'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # inherited from CreateModelMixin

        # Assign the user to multiple properties of the Program
        group_program_admin = Group.objects.get(name=ROLE_PROGRAM_ADMIN)
        wflvl1 = WorkflowLevel1.objects.get(
            level1_uuid=serializer.data['level1_uuid'])
        wflvl1.organization = request.user.tola_user.organization
        wflvl1.user_access.add(request.user.tola_user)
        wflvl1.save()
        WorkflowTeam.objects.create(
            workflow_user=request.user.tola_user, workflowlevel1=wflvl1,
            role=group_program_admin)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, pk):
        workflowlevel1 = self.get_object()
        workflowlevel1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ordering_fields = ('country__country', 'name')
    filter_fields = ('country__country', 'name', 'level1_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = WorkflowLevel1.objects.all().annotate(
        budget=Sum('workflowlevel2__total_estimated_budget'),
        actuals=Sum('workflowlevel2__actual_cost'))
    permission_classes = (AllowTolaRoles, IsOrgMember)
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
    permission_classes = (IsOrgMember,)
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    def list(self, request):

        if request.user.is_superuser:
            queryset = Office.objects.all()
        else:
            queryset = Office.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('country__country',)
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
        if request.user.is_superuser:
            queryset = SiteProfile.objects.all()
        else:
            tola_user = TolaUser.objects.get(user=request.user)
            queryset = SiteProfile.objects.filter(organization=tola_user.organization)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        user_org = TolaUser.objects.get(user=user).organization
        serializer.save(organization=user_org, created_by=self.request.user)

    filter_fields = ('country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = SiteProfile .objects.all()
    serializer_class = SiteProfileSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):

        queryset = Country.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
            queryset = Indicator.objects.all().annotate(
                actuals=Sum('collecteddata__achieved'))
        else:
            user_level1 = getLevel1(request.user)
            queryset = Indicator.objects.all().filter(
                workflowlevel1__in=user_level1).annotate(
                actuals=Sum('collecteddata__achieved'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        indicator = self.get_object()
        indicator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return Indicator.objects.annotate(
            actuals=Sum('collecteddata__achieved'))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__country__country', 'workflowlevel1__name',
                     'indicator_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles,)
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


class FrequencyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        organization = TolaUser.objects.get(user=request.user).organization
        queryset = Frequency.objects.filter(organization=organization)
        serializer = FrequencySerializer(instance=queryset,
                                         context={'request': request},
                                         many=True)
        return Response(serializer.data)

    permission_classes = (IsOrgMember,)
    queryset = Frequency.objects.all()
    serializer_class = FrequencySerializer


class TolaUserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving TolaUsers.

    """
    def list(self, request):
        queryset = TolaUser.objects.all()
        serializer = TolaUserSerializer(
            instance=queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TolaUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TolaUserSerializer(instance=user,
                                        context={'request': request})
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
    permission_classes = (IsOrgMember,)
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
            queryset = Objective.objects.all().filter(
                workflowlevel1__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
    permission_classes = (IsOrgMember,)
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
            queryset = DisaggregationType.objects.all().filter(
                organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('organization__id', 'country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)

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

        user_level1 = getLevel1(request.user)
        queryset = Stakeholder.objects.all().filter(
            workflowlevel1__in=user_level1)

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

    def perform_create(self, serializer):
        user = self.request.user
        user_org = TolaUser.objects.get(user=user).organization
        serializer.save(organization=user_org, created_by=self.request.user)

    filter_fields = ('workflowlevel1__name',)
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
            queryset = ExternalService.objects.all().filter(
                organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
            tola_user = TolaUser.objects.get(user=request.user)
            queryset = StrategicObjective.objects.filter(
                organization=tola_user.organization)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        user_org = TolaUser.objects.get(user=user).organization
        serializer.save(organization=user_org)

    filter_fields = ('organization__id', 'country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
            queryset = StakeholderType.objects.all().filter(
                organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
    permission_classes = (IsOrgMember,)
    queryset = ProfileType.objects.all()
    serializer_class = ProfileTypeSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AdminLevelOne.objects.all()
    serializer_class = ProvinceSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AdminLevelTwo.objects.all()
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
    queryset = AdminLevelFour.objects.all()
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
            user_level1 = getLevel1(request.user)
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Contact.objects.filter(organization=user_org,
                                              workflowlevel1__in=user_level1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('name', 'stakeholder__organization__id', 'stakeholder')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
            user_level1 = getLevel1(request.user)
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Documentation.objects.all().filter(
                workflowlevel2__workflowlevel1__organization=user_org).filter(
                workflowlevel1__in=user_level1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel2__workflowlevel1__country__country',
                     'workflowlevel2__workflowlevel1__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
        if request.user.is_superuser:
            queryset = CollectedData.objects.all()
        else:
            user_level1 = getLevel1(request.user)
            queryset = CollectedData.objects.all().filter(
                indicator__workflowlevel1__in=user_level1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('indicator__workflowlevel1__country__country',
                     'indicator__workflowlevel1__name', 'indicator',
                     'indicator__workflowlevel1__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = CollectedData.objects.all()
    permission_classes = (AllowTolaRoles, IsOrgMember)
    serializer_class = CollectedDataSerializer
    pagination_class = SmallResultsSetPagination


class TolaTableViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_level1 = getLevel1(self.request.user)
        queryset = TolaTable.objects.filter(workflowlevel1__in=user_level1)
        table_id = self.request.query_params.get('table_id', None)
        if table_id is not None:
            queryset = queryset.filter(table_id=table_id)
        return queryset

    filter_fields = ('table_id', 'country__country',
                     'collecteddata__indicator__workflowlevel1__name',
                     'organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = TolaTableSerializer
    permission_classes = (IsOrgMember,)
    pagination_class = StandardResultsSetPagination
    queryset = TolaTable.objects.all()


class DisaggregationValueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        queryset = DisaggregationValue.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('disaggregation_label__disaggregation_type',)
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

    def list(self, request):
        if request.user.is_superuser:
            queryset = Checklist.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Checklist.objects.all().filter(
                workflowlevel2__workflowlevel1__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_fields = ('workflowlevel2__name',
                     'workflowlevel2__workflowlevel1__organization__id',
                     'workflowlevel2__workflowlevel1__country__country',
                     'owner')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class OrganizationViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Organization.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Organization.objects.filter(id=user_org.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
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
        if request.user.is_superuser:
            queryset = WorkflowLevel2.objects.all()
        else:
            user_level1 = getLevel1(request.user)
            queryset = WorkflowLevel2.objects.all().filter(
                workflowlevel1__in=user_level1)

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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    """
    def post(self,request):

        for each agreement
            insert int and string fields direct
            if FK field

        return blank
    """

    filter_fields = ('workflowlevel1__country__country', 'workflowlevel1__name',
                     'level2_uuid', 'workflowlevel1__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = WorkflowLevel2.objects.all()
    permission_classes = (AllowTolaRoles, IsOrgMember)
    serializer_class = WorkflowLevel2Serializer
    pagination_class = SmallResultsSetPagination


class WorkflowModulesViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = WorkflowModules.objects.all()
    serializer_class = WorkflowModulesSerializer


class WorkflowLevel2SortViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = WorkflowLevel2Sort.objects.all()
        else:
            user_level1 = getLevel1(request.user)
            queryset = WorkflowLevel2Sort.objects.all().filter(
                workflowlevel1__in=user_level1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = WorkflowLevel2Sort.objects.all()
    permission_classes = (IsOrgMember,)
    serializer_class = WorkflowLevel2SortSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ApprovalTypeViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = ApprovalType.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = ApprovalType.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = ApprovalType.objects.all()
    serializer_class = ApprovalTypeSerializer


class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BeneficiaryViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Beneficiary.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Beneficiary.objects.all().filter(
                workflowlevel1__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer


class DistributionViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Distribution.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Distribution.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer


class CustomFormViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = CustomForm.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = CustomForm.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = CustomForm.objects.all()
    serializer_class = CustomFormSerializer


class CustomFormFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomFormField.objects.all()
    serializer_class = CustomFormFieldSerializer


class FieldTypeViewSet(viewsets.ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer


class BudgetViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Budget.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Budget.objects.all().filter(
                workflowlevel2__workflowlevel1__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class RiskRegisterViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = RiskRegister.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = RiskRegister.objects.all().filter(
                workflowlevel2__workflowlevel1__organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = RiskRegister.objects.all()
    permission_classes = (IsOrgMember,)
    serializer_class = RiskRegisterSerializer


class CodedFieldViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = CodedField.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = CodedField.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = CodedField.objects.all()
    serializer_class = CodedFieldSerializer


class CodedFieldValuesViewSet(viewsets.ModelViewSet):
    queryset = CodedFieldValues.objects.all()
    serializer_class = CodedFieldValuesSerializer


class IssueRegisterViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = IssueRegister.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = IssueRegister.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        user_org = TolaUser.objects.get(user=user).organization
        serializer.save(organization=user_org)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = IssueRegister.objects.all()
    serializer_class = IssueRegisterSerializer


class LandTypeViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """

    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer


class InternationalizationViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """

    queryset = Internationalization.objects.all()
    serializer_class = InternationalizationSerializer


class TolaUserFilterViewSet(viewsets.ModelViewSet):
    queryset = TolaUserFilter.objects.all()
    serializer_class = TolaUserFilterSerializer


class AwardViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Award.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Award.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class WorkflowTeamViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = WorkflowTeam.objects.all()
        else:
            user_level1 = getLevel1(request.user)
            queryset = WorkflowTeam.objects.all().filter(
                workflowlevel1__in=user_level1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = WorkflowTeam.objects.all()
    serializer_class = WorkflowTeamSerializer


class MilestoneViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Milestone.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Milestone.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


class PortfolioViewSet(viewsets.ModelViewSet):

    def list(self, request):
        if request.user.is_superuser:
            queryset = Portfolio.objects.all()
        else:
            user_org = TolaUser.objects.get(user=request.user).organization
            queryset = Portfolio.objects.all().filter(organization=user_org)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class SectorRelatedViewSet(viewsets.ModelViewSet):

    filter_fields = ('sector', 'organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = SectorRelated.objects.all()
    serializer_class = SectorRelatedSerializer


class WorkflowLevel1SectorViewSet(viewsets.ModelViewSet):

    queryset = WorkflowLevel1Sector.objects.all()
    filter_fields = ('sector', 'workflowlevel1',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = WorkflowLevel1SectorSerializer
