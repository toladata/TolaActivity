from rest_framework import permissions
from rest_framework.relations import ManyRelatedField

from workflow.models import *
from indicators.models import *
from formlibrary.models import *


class UserIsOwnerOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated()
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def check_object_permission(self, user, obj):
        return (user and user.is_authenticated() and
                (user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)


class IsOrgMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Object level permissions are used to determine if a user
        should be allowed to act on a particular object
        """

        if request.user.is_superuser:
            return True
        user_org = request.user.tola_user.organization

        try:
            if obj.__class__ in [Sector, ProjectType, SiteProfile, Frequency,
                                 FundCode, DisaggregationType, Level,
                                 ExternalService, StrategicObjective,
                                 StakeholderType, ProfileType, Contact,
                                 ApprovalType, Distribution, CustomForm,
                                 CodedField, IssueRegister, Award, Milestone,
                                 Portfolio, WorkflowLevel1]:
                return obj.organization == user_org
            elif obj.__class__ in [Objective, Beneficiary, Documentation,
                                   CollectedData]:
                return obj.workflowlevel1.organization == user_org
            elif obj.__class__ in [Checklist, Budget, RiskRegister]:
                return obj.workflowlevel2.workflowlevel1.organization == \
                       user_org
            elif obj.__class__ in [Organization]:
                return obj == user_org
            elif obj.__class__ in [WorkflowTeam]:
                return obj.partner_org == user_org
            elif obj.__class__ in [Indicator]:
                return obj.workflowlevel1.all().filter(
                    organization=user_org).exists()
        except AttributeError:
            pass
        return False


class AllowTolaRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        user_groups = request.user.groups.values_list('name', flat=True)
        if ROLE_ORGANIZATION_ADMIN in user_groups:
            return True

        if view.action == 'create' and 'workflowlevel1' in request.data:
            user_org = request.user.tola_user.organization
            queryset = self._queryset(view)
            model_cls = queryset.model
            wflvl1_serializer = view.serializer_class().get_fields()['workflowlevel1']

            # Check if the field is Many-To-Many or not
            if wflvl1_serializer.__class__ == ManyRelatedField:
                primitive_value = request.data.getlist('workflowlevel1')
            else:
                primitive_value = request.data.get('workflowlevel1')

            # Get objects using their URLs
            wflvl1 = wflvl1_serializer.run_validation(primitive_value)

            # We use a list to fetch the program teams
            if not isinstance(wflvl1, list):
                wflvl1 = [wflvl1]
            team_groups = WorkflowTeam.objects.filter(
                workflow_user=request.user.tola_user,
                workflowlevel1__in=wflvl1).values_list('role__name', flat=True)

            if model_cls.__name__ in ['Contact', 'Documentation',
                                      'Indicator', 'CollectedData',
                                      'Level', 'Objective',
                                      'WorkflowLevel2']:
                return (ROLE_VIEW_ONLY not in team_groups and
                        self._check_organization(wflvl1, user_org))
            elif model_cls.__name__ == 'WorkflowTeam':
                return (ROLE_VIEW_ONLY not in team_groups and
                        ROLE_PROGRAM_TEAM not in team_groups and
                        self._check_organization(wflvl1, user_org))
        return True

    def _check_organization(self, workflowlevel1s, organization):
        """
        Check if the organization passed matches with one of the programs
        :param workflowlevel1s:
        :param organization:
        :return: boolean
        """
        for wflvl1 in workflowlevel1s:
            if wflvl1.organization == organization:
                return True
        return False

    def _queryset(self, view):
        """
        Return the queryset of the view
        :param view:
        :return: QuerySet
        """
        assert hasattr(view, 'get_queryset') \
            or getattr(view, 'queryset', None) is not None, (
            'Cannot apply {} on a view that does not set '
            '`.queryset` or have a `.get_queryset()` method.'
        ).format(self.__class__.__name__)

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
            assert queryset is not None, (
                '{}.get_queryset() returned None'.format(
                    view.__class__.__name__)
            )
            return queryset
        return view.queryset

    def has_object_permission(self, request, view, obj):
        """
        Object level permissions are used to determine if a user
        should be allowed to act on a particular object
        """
        if request.user and request.user.is_authenticated():
            if request.user.is_superuser:
                return True
            user_groups = request.user.groups.values_list('name', flat=True)
            if ROLE_ORGANIZATION_ADMIN in user_groups:
                return True

            queryset = self._queryset(view)
            model_cls = queryset.model
            if model_cls.__name__ == 'Portfolio':
                team_groups = WorkflowTeam.objects.filter(
                    workflow_user=request.user.tola_user,
                    workflowlevel1__portfolio=obj).values_list(
                    'role__name', flat=True)
                if ROLE_PROGRAM_ADMIN in team_groups or ROLE_PROGRAM_TEAM in \
                        team_groups:
                    return view.action == 'retrieve'
            elif model_cls.__name__ == 'WorkflowTeam':
                if ROLE_PROGRAM_ADMIN == obj.role.name:
                    return True
                else:
                    return view.action == 'retrieve'
            elif model_cls.__name__ == 'WorkflowLevel1':
                team_groups = WorkflowTeam.objects.filter(
                    workflow_user=request.user.tola_user,
                    workflowlevel1=obj).values_list(
                    'role__name', flat=True)
                if ROLE_PROGRAM_ADMIN in team_groups:
                    return True
                elif ROLE_PROGRAM_TEAM in team_groups:
                    return view.action != 'destroy'
            elif model_cls.__name__ == 'Indicator':
                team_groups = WorkflowTeam.objects.filter(
                    workflow_user=request.user.tola_user,
                    workflowlevel1__indicator=obj).values_list(
                    'role__name', flat=True)
                if ROLE_PROGRAM_ADMIN in team_groups:
                    return True
                elif ROLE_PROGRAM_TEAM in team_groups:
                    return view.action != 'destroy'
                elif ROLE_VIEW_ONLY in team_groups:
                    return view.action == 'retrieve'
            elif model_cls.__name__ in ['CollectedData', 'Level',
                                        'WorkflowLevel2']:
                team_groups = WorkflowTeam.objects.filter(
                    workflow_user=request.user.tola_user,
                    workflowlevel1=obj.workflowlevel1).values_list(
                    'role__name', flat=True)
                if ROLE_PROGRAM_ADMIN in team_groups:
                    return True
                elif ROLE_PROGRAM_TEAM in team_groups:
                    return view.action != 'destroy'
                elif ROLE_VIEW_ONLY in team_groups:
                    return view.action == 'retrieve'
            else:
                return True

        return False
