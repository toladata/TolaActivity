from rest_framework import permissions

from tola.util import getLevel1
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
        if request.user.is_superuser:
            return True
        user_org = request.user.tola_user.organization

        if obj.__class__ in [Sector, ProjectType, SiteProfile, Frequency,
                             IndicatorType, FundCode, DisaggregationType,
                             Level, ExternalService, StrategicObjective,
                             StakeholderType, ProfileType, Contact,
                             ApprovalType, Distribution, CustomForm,
                             CodedField, IssueRegister, Award, Milestone,
                             Portfolio]:
            return obj.organization == user_org
        elif obj.__class__ in [Objective, Beneficiary]:
            return obj.workflowlevel1.organization == user_org
        elif obj.__class__ in [Checklist, Budget, RiskRegister]:
            return obj.workflowlevel2.workflowlevel1.organization == user_org
        elif obj.__class__ in [Organization, ]:
            return obj == user_org

        return False


class IsProgramMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        user_level1 = getLevel1(request.user)

        if obj.__class__ in [CollectedData, ]:
            return obj.indicator.workflowlevel1 in user_level1
        elif obj.__class__ in [WorkflowLevel1, ]:
            user_groups = request.user.groups.values_list('name', flat=True)
            if ROLE_ORGANIZATION_ADMIN in user_groups:
                user_org = request.user.tola_user.organization
                return obj.organization == user_org
            return obj in user_level1
        elif obj.__class__ in [Indicator, Stakeholder, TolaTable,
                             WorkflowLevel2, WorkflowLevel2Sort,
                             WorkflowTeam]:
            return obj.workflowlevel1 in user_level1

        return False


class IsOrgProgramMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        user_org = request.user.tola_user.organization
        user_level1 = getLevel1(request.user)

        if obj.__class__ in [Contact, ]:
            return obj.organization == user_org and obj.workflowlevel1 in \
                    user_level1
        elif obj.__class__ in [Documentation, ]:
            return obj.workflowlevel2.workflowlevel1.organization == user_org \
                    and obj.workflowlevel1 in user_level1

        return False


class AllowTolaRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        user_groups = request.user.groups.values_list('name', flat=True)
        team_groups = WorkflowTeam.objects.filter(
            workflow_user=request.user.tola_user).order_by('role__name').\
            distinct('role__name').values_list('role__name', flat=True)

        if ROLE_ORGANIZATION_ADMIN in user_groups:
            return True
        elif ROLE_PROGRAM_ADMIN in team_groups or ROLE_PROGRAM_TEAM in \
                team_groups:
            return True
        elif ROLE_VIEW_ONLY in team_groups and request.method in \
                permissions.SAFE_METHODS:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated():
            if request.user.is_superuser:
                return True
            user_groups = request.user.groups.values_list('name', flat=True)
            team_groups = WorkflowTeam.objects.filter(
                workflow_user=request.user.tola_user).order_by('role__name').\
                distinct('role__name').values_list('role__name', flat=True)

            if ROLE_ORGANIZATION_ADMIN in user_groups:
                return True
            elif ROLE_PROGRAM_ADMIN in team_groups:
                if obj.__class__ == Portfolio:
                    return view.action in ['retrieve', 'list']
                if obj.__class__ == WorkflowLevel1:
                    if view.action == 'destroy':
                        return obj.created_by == request.user
                return True
            elif ROLE_PROGRAM_TEAM in team_groups:
                if obj.__class__ in [CollectedData, CustomForm, Indicator,
                                     Level, WorkflowLevel2]:
                    if view.action == 'destroy':
                        return obj.created_by == request.user
                    return True
                if obj.__class__ in [Portfolio, WorkflowLevel1]:
                    return view.action in ['create', 'update', 'partial_update']
            elif ROLE_VIEW_ONLY in team_groups:
                if obj.__class__ in [CollectedData, Level, WorkflowLevel2]:
                    wf_team = WorkflowTeam.objects.get(
                        workflow_user=request.user.tola_user,
                        role__name=ROLE_VIEW_ONLY)
                    res = obj.__class__.objects.filter(
                        workflowlevel1=wf_team.workflowlevel1)
                    return obj in res
                if obj.__class__ == Indicator:
                    wf_team = WorkflowTeam.objects.filter(
                        workflow_user=request.user.tola_user,
                        workflowlevel1__indicator__in=obj,
                        role__name=ROLE_VIEW_ONLY)
                    if wf_team:
                        return True
                    else:
                        return False
        return False
