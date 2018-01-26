import json
import logging
from urlparse import urljoin

from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import django_filters
import requests
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from formlibrary.models import (
    Beneficiary, CustomForm, CustomFormField, FieldType)
from indicators.models import (
    Indicator, Frequency, IndicatorType, Objective, DisaggregationType,
    Level, ExternalService, ExternalServiceRecord, StrategicObjective,
    PeriodicTarget, CollectedData, TolaTable, DisaggregationValue,
    DisaggregationLabel)

from workflow import models as wfm
from .permissions import IsOrgMember, AllowTolaRoles
from . import serializers

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class ProgramIndicatorReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProgramIndicatorSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = wfm.WorkflowLevel1.objects.prefetch_related(
            'indicator_set',
            'indicator_set__indicator_type',
            'indicator_set__sector', 'indicator_set__level',
            'indicator_set__collecteddata_set').all()
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = wfm.User.objects.all()
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = wfm.Group.objects.all()
    serializer_class = serializers.GroupSerializer


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
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset()).annotate(
            budget=Sum('workflowlevel2__total_estimated_budget'),
            actuals=Sum('workflowlevel2__actual_cost'))
        if not request.user.is_superuser:
            if wfm.ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list(
                    'name', flat=True):
                organization_id = wfm.TolaUser.objects. \
                    values_list('organization_id', flat=True). \
                    get(user=request.user)
                queryset = queryset.filter(organization_id=organization_id)
            else:
                wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                    workflow_user__user=request.user).values_list(
                    'workflowlevel1__id', flat=True)
                queryset = queryset.filter(id__in=wflvl1_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # inherited from CreateModelMixin

        # Assign the user to multiple properties of the Program
        group_program_admin = Group.objects.get(name=wfm.ROLE_PROGRAM_ADMIN)
        wflvl1 = wfm.WorkflowLevel1.objects.get(
            level1_uuid=serializer.data['level1_uuid'])
        wfm.WorkflowTeam.objects.create(
            workflow_user=request.user.tola_user, workflowlevel1=wflvl1,
            role=group_program_admin)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        obj = serializer.save(organization_id=organization_id)
        obj.user_access.add(self.request.user.tola_user)

    def destroy(self, request, pk):
        workflowlevel1 = self.get_object()
        workflowlevel1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    ordering_fields = ('country__country', 'name')
    filter_fields = ('country__country', 'name', 'level1_uuid')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    queryset = wfm.WorkflowLevel1.objects.all().annotate(
        budget=Sum('workflowlevel2__total_estimated_budget'),
        actuals=Sum('workflowlevel2__actual_cost'))
    permission_classes = (AllowTolaRoles, IsOrgMember)
    serializer_class = serializers.WorkflowLevel1Serializer


class SectorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def __get__(self, instance, owner):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not self.request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=self.request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.Sector.objects.all()
    serializer_class = serializers.SectorSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.ProjectType.objects.all()
    serializer_class = serializers.ProjectTypeSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    filter_fields = ('country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.Office.objects.all()
    serializer_class = serializers.OfficeSerializer


class SiteProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by country name and program name
    limit to users logged in country permissions
    """
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id,
                        created_by=self.request.user)

    filter_fields = ('country__country',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.SiteProfile.objects.all()
    serializer_class = serializers.SiteProfileSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class IndicatorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Search by country name and program name
    limit to users logged in country permissions
    """
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            if wfm.ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list(
                    'name', flat=True):
                organization_id = wfm.TolaUser.objects. \
                    values_list('organization_id', flat=True). \
                    get(user=request.user)
                queryset = queryset.filter(
                    workflowlevel1__organization_id=organization_id)
            else:
                wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                    workflow_user__user=request.user).values_list(
                    'workflowlevel1__id', flat=True)
                queryset = queryset.filter(
                    workflowlevel1__in=wflvl1_ids).annotate(
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
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = Indicator.objects.all()
    serializer_class = serializers.IndicatorSerializer


class FrequencyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        organization_id = wfm.TolaUser.objects.\
                values_list('organization_id', flat=True).\
                get(user=request.user)
        queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(instance=queryset,
                                         context={'request': request},
                                         many=True)
        return Response(serializer.data)

    permission_classes = (IsOrgMember,)
    queryset = Frequency.objects.all()
    serializer_class = serializers.FrequencySerializer


class TolaUserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving wfm.TolaUsers.

    """
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects.\
                values_list('organization_id', flat=True).\
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(
            instance=queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance=user,
                                        context={'request': request})
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.TolaUser.objects.all()
    serializer_class = serializers.TolaUserSerializer


class IndicatorTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects.\
                values_list('organization_id', flat=True).\
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = IndicatorType.objects.all()
    serializer_class = serializers.IndicatorTypeSerializer


class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel1__organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = Objective.objects.all()
    serializer_class = serializers.ObjectiveSerializer


class FundCodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.FundCode.objects.all()
    serializer_class = serializers.FundCodeSerializer


class DisaggregationTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id)

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = DisaggregationType.objects.all()
    serializer_class = serializers.DisaggregationTypeSerializer


class LevelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('organization__id', 'country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)

    queryset = Level.objects.all()
    serializer_class = serializers.LevelSerializer


class StakeholderViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        wflvl1_ids = wfm.WorkflowTeam.objects.filter(
            workflow_user__user=request.user).values_list(
            'workflowlevel1__id', flat=True)
        queryset = queryset.filter(workflowlevel1__in=wflvl1_ids).distinct()

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = serializers.StakeholderFullSerializer

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = serializers.StakeholderFullSerializer

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id,
                        created_by=self.request.user)

    filter_fields = ('workflowlevel1__name',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.Stakeholder.objects.all()
    serializer_class = serializers.StakeholderSerializer


class ExternalServiceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = ExternalService.objects.all()
    serializer_class = serializers.ExternalServiceSerializer


class ExternalServiceRecordViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = ExternalServiceRecord.objects.all()
    serializer_class = serializers.ExternalServiceRecordSerializer


class StrategicObjectiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id)

    filter_fields = ('organization__id', 'country__country')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = StrategicObjective.objects.all()
    serializer_class = serializers.StrategicObjectiveSerializer


class StakeholderTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.StakeholderType.objects.all()
    serializer_class = serializers.StakeholderTypeSerializer


class ProfileTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.ProfileType.objects.all()
    serializer_class = serializers.ProfileTypeSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = wfm.AdminLevelOne.objects.all()
    serializer_class = serializers.ProvinceSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = wfm.AdminLevelTwo.objects.all()
    serializer_class = serializers.DistrictSerializer


class AdminLevelThreeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = wfm.AdminLevelThree.objects.all()
    serializer_class = serializers.AdminLevelThreeSerializer


class VillageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = wfm.AdminLevelFour.objects.all()
    serializer_class = serializers.VillageSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                workflow_user__user=request.user).values_list(
                'workflowlevel1__id', flat=True)
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id,
                                       workflowlevel1__in=wflvl1_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('name',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = wfm.Contact.objects.all()
    serializer_class = serializers.ContactSerializer


class DocumentationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                workflow_user__user=request.user).values_list(
                'workflowlevel1__id', flat=True)
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel1__organization_id=organization_id
            ).filter(
                workflowlevel1__in=wflvl1_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__country__country',
                     'workflowlevel1__organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.Documentation.objects.all()
    serializer_class = serializers.DocumentationSerializer


class PeriodicTargetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = PeriodicTarget.objects.all()
    serializer_class = serializers.PeriodicTargetSerializer


class CollectedDataViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                workflow_user__user=request.user).values_list(
                'workflowlevel1__id', flat=True)
            queryset = queryset.filter(indicator__workflowlevel1__in=wflvl1_ids)
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
    serializer_class = serializers.CollectedDataSerializer
    pagination_class = SmallResultsSetPagination


class TolaTableViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    def get_queryset(self):
        wflvl1_ids = wfm.WorkflowTeam.objects.filter(
            workflow_user__user=self.request.user).values_list(
            'workflowlevel1__id', flat=True)
        queryset = TolaTable.objects.filter(workflowlevel1__in=wflvl1_ids)
        table_id = self.request.query_params.get('table_id', None)
        if table_id is not None:
            queryset = queryset.filter(table_id=table_id)
        return queryset

    filter_fields = ('table_id', 'country__country',
                     'collecteddata__indicator__workflowlevel1__name',
                     'organization__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.TolaTableSerializer
    permission_classes = (IsOrgMember,)
    pagination_class = StandardResultsSetPagination
    queryset = TolaTable.objects.all()


class DisaggregationValueViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    filter_fields = ('disaggregation_label__disaggregation_type',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = DisaggregationValue.objects.all()
    serializer_class = serializers.DisaggregationValueSerializer


class DisaggregationLabelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = DisaggregationLabel.objects.all()
    serializer_class = serializers.DisaggregationLabelSerializer


class ChecklistViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel2__workflowlevel1__organization_id=organization_id)
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
    queryset = wfm.Checklist.objects.all()
    serializer_class = serializers.ChecklistSerializer


class OrganizationViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


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
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            if wfm.ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list(
                    'name', flat=True):
                queryset = queryset.filter(
                    workflowlevel1__organization_id=organization_id)
            else:
                wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                    workflow_user__user=request.user).values_list(
                    'workflowlevel1__id', flat=True)
                queryset = queryset.filter(
                    workflowlevel1__organization_id=organization_id,
                    workflowlevel1__in=wflvl1_ids)

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = serializers.WorkflowLevel2FullSerializer

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        nested = request.GET.get('nested_models')
        if nested is not None and (nested.lower() == 'true' or nested == '1'):
            self.serializer_class = serializers.WorkflowLevel2FullSerializer

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel1__country__country', 'workflowlevel1__name',
                     'level2_uuid', 'workflowlevel1__id')
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.WorkflowLevel2.objects.all()
    permission_classes = (AllowTolaRoles, IsOrgMember)
    serializer_class = serializers.WorkflowLevel2Serializer
    pagination_class = SmallResultsSetPagination


class WorkflowModulesViewSet(viewsets.ModelViewSet):
    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.WorkflowModules.objects.all()
    serializer_class = serializers.WorkflowModulesSerializer


class WorkflowLevel2SortViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                workflow_user__user=request.user).values_list(
                'workflowlevel1__id', flat=True)
            queryset = queryset.filter(workflowlevel1__in=wflvl1_ids)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = wfm.WorkflowLevel2Sort.objects.all()
    permission_classes = (IsOrgMember,)
    serializer_class = serializers.WorkflowLevel2SortSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """
    queryset = wfm.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class ApprovalTypeViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.ApprovalType.objects.all()
    serializer_class = serializers.ApprovalTypeSerializer


class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = wfm.ApprovalWorkflow.objects.all()
    serializer_class = serializers.ApprovalWorkflowSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BeneficiaryViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel1__organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = Beneficiary.objects.all()
    serializer_class = serializers.BeneficiarySerializer


class CustomFormViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        form_data = request.data.copy()
        fields = form_data.get('fields')
        headers = {
            'Authorization': 'Token {}'.format(
                settings.TOLA_TRACK_TOKEN),
        }

        if isinstance(fields, list):
            fields = json.dumps(fields)

        # Serialize the program
        if request.data.get('workflowlevel1'):
            wflvl1_serializer = self.serializer_class().get_fields()[
                'workflowlevel1']
            wkfl1 = wflvl1_serializer.run_validation(request.data.get(
                'workflowlevel1'))
        else:
            wkfl1 = None

        if instance.workflowlevel1:
            if wkfl1 and wkfl1 != instance.workflowlevel1:
                return Response({'detail': 'You cannot change the Program.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if there is already data in the table
            url_subpath = 'api/customform/%s/has_data' % instance.silo_id
            url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
            response = requests.get(url, headers=headers)
            has_data = json.loads(response.content)

            if has_data == 'false':
                # Update the table info in Track
                data = {'name': form_data.get('name'),
                        'description': form_data.get('description'),
                        'fields': fields}
                url_subpath = 'api/customform/%s' % instance.silo_id
                url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
                requests.put(url, data=data, headers=headers)
            else:
                return Response(
                    {'detail': 'You already have data in the instance.'},
                    status=status.HTTP_409_CONFLICT
                )
        elif wkfl1:
            tola_user = request.user.tola_user
            silo_data = {'name': form_data.get('name'),
                         'description': form_data.get('description'),
                         'fields': fields,
                         'level1_uuid': wkfl1.level1_uuid,
                         'tola_user_uuid': tola_user.tola_user_uuid}

            # Make a POST request to Track to create a table
            url_subpath = 'api/customform'
            url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
            response = requests.post(url, data=silo_data, headers=headers)

            silo_json = json.loads(response.content)
            form_data['silo_id'] = silo_json.get('id')

        serializer = self.get_serializer(instance, data=form_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id,
                        created_by=self.request.user)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = CustomForm.objects.all()
    serializer_class = serializers.CustomFormSerializer


class CustomFormFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomFormField.objects.all()
    serializer_class = serializers.CustomFormFieldSerializer


class FieldTypeViewSet(viewsets.ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = serializers.FieldTypeSerializer


class BudgetViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel2__workflowlevel1__organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.Budget.objects.all()
    serializer_class = serializers.BudgetSerializer


class RiskRegisterViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(
                workflowlevel2__workflowlevel1__organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = wfm.RiskRegister.objects.all()
    permission_classes = (IsOrgMember,)
    serializer_class = serializers.RiskRegisterSerializer


class CodedFieldViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.CodedField.objects.all()
    serializer_class = serializers.CodedFieldSerializer


class CodedFieldValuesViewSet(viewsets.ModelViewSet):
    queryset = wfm.CodedFieldValues.objects.all()
    serializer_class = serializers.CodedFieldValuesSerializer


class IssueRegisterViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        organization_id = wfm.TolaUser.objects. \
            values_list('organization_id', flat=True). \
            get(user=self.request.user)
        serializer.save(organization_id=organization_id)

    filter_fields = ('workflowlevel2__workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.IssueRegister.objects.all()
    serializer_class = serializers.IssueRegisterSerializer


class LandTypeViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """

    queryset = wfm.LandType.objects.all()
    serializer_class = serializers.LandTypeSerializer


class InternationalizationViewSet(viewsets.ModelViewSet):
    """
    Global Field so do not filter by Org
    """

    queryset = wfm.Internationalization.objects.all()
    serializer_class = serializers.InternationalizationSerializer


class TolaUserFilterViewSet(viewsets.ModelViewSet):
    queryset = wfm.TolaUserFilter.objects.all()
    serializer_class = serializers.TolaUserFilterSerializer


class AwardViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (IsOrgMember,)
    queryset = wfm.Award.objects.all()
    serializer_class = serializers.AwardSerializer


class WorkflowTeamViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update` and
    `destroy` actions.
    """
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            if wfm.ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list(
                    'name', flat=True):
                organization_id = wfm.TolaUser.objects. \
                    values_list('organization_id', flat=True). \
                    get(user=request.user)
                queryset = queryset.filter(
                    workflow_user__organization_id=organization_id)
            else:
                wflvl1_ids = wfm.WorkflowTeam.objects.filter(
                    workflow_user__user=request.user).values_list(
                    'workflowlevel1__id', flat=True)
                queryset = queryset.filter(workflowlevel1__in=wflvl1_ids)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('workflowlevel1__organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (AllowTolaRoles,)
    queryset = wfm.WorkflowTeam.objects.all()
    serializer_class = serializers.WorkflowTeamSerializer


class MilestoneViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    permission_classes = (IsOrgMember,)
    queryset = wfm.Milestone.objects.all()
    serializer_class = serializers.MilestoneSerializer


class PortfolioViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # inherited from CreateModelMixin

        portfolio = wfm.Portfolio.objects.get(pk=serializer.data['id'])
        portfolio.organization = request.user.tola_user.organization
        portfolio.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    permission_classes = (AllowTolaRoles, IsOrgMember)
    queryset = wfm.Portfolio.objects.all()
    serializer_class = serializers.PortfolioSerializer


class PublicDashboardViewSet(viewsets.ModelViewSet):

    queryset = wfm.Dashboard.objects.all().filter(public_all=True)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.PublicDashboardSerializer


class PublicOrgDashboardViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            organization_id = wfm.TolaUser.objects. \
                values_list('organization_id', flat=True). \
                get(user=request.user)
            queryset = queryset.filter(organization_id=organization_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = wfm.Dashboard.objects.all().filter(public_in_org=True)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.PublicOrgDashboardSerializer


class DashboardViewSet(viewsets.ModelViewSet):

    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            get_user = wfm.TolaUser.objects.get(user=request.user)
            queryset = queryset.filter(Q(user=get_user) | Q(share=get_user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('user', 'share',)
    queryset = wfm.Dashboard.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.DashboardSerializer


class WidgetViewSet(viewsets.ModelViewSet):
    def list(self, request):
        # Use this queryset or the django-filters lib will not work
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    filter_fields = ('dashboard',)
    queryset = wfm.Widget.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.WidgetSerializer


class SectorRelatedViewSet(viewsets.ModelViewSet):

    filter_fields = ('sector', 'organization__id',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    queryset = wfm.SectorRelated.objects.all()
    serializer_class = serializers.SectorRelatedSerializer


class WorkflowLevel1SectorViewSet(viewsets.ModelViewSet):

    queryset = wfm.WorkflowLevel1Sector.objects.all()
    filter_fields = ('sector', 'workflowlevel1',)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    serializer_class = serializers.WorkflowLevel1SectorSerializer
