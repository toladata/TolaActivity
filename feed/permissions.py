from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import permissions

from tola.util import getLevel1
from workflow.models import (
    TolaUser, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM,
    WorkflowTeam)


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


class WorkflowLevel1Permissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
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
        user_level1 = getLevel1(request.user)
        if view.action == 'list':
            user_org = TolaUser.objects.get(user=request.user).organization
            user_groups = request.user.groups.values_list('name', flat=True)
            return (request.user.is_authenticated() and
                    (obj in user_level1 and obj.organization in user_org
                     or ROLE_ORGANIZATION_ADMIN in user_groups))
        if view.action == 'retrieve':
            user_groups = request.user.groups.values_list('name', flat=True)
            return (request.user.is_authenticated() and
                    (obj in user_level1 or
                     ROLE_ORGANIZATION_ADMIN in user_groups))
        elif view.action in ['update', 'partial_update', 'destroy']:
            if request.user.is_superuser:
                return True

            if obj.organization != request.user.tola_user.organization:
                return False

            user_groups = request.user.groups.values_list('name', flat=True)
            if ROLE_ORGANIZATION_ADMIN in user_groups:
                return True

            if view.action == 'destroy':
                try:
                    WorkflowTeam.objects.get(
                        workflow_user=request.user.tola_user,
                        workflowlevel1=obj,
                        role__name=ROLE_PROGRAM_ADMIN)
                except WorkflowTeam.DoesNotExist:
                    return False
                else:
                    return True
            else:
                try:
                    WorkflowTeam.objects.get(
                        Q(role__name=ROLE_PROGRAM_ADMIN) |
                        Q(role__name=ROLE_PROGRAM_TEAM),
                        workflow_user=request.user.tola_user,
                        workflowlevel1=obj)
                except WorkflowTeam.DoesNotExist:
                    return False
                else:
                    return True

        else:
            return False


class IndicatorPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'list':
            # TODO Ticket: #793
            return True
        if view.action == 'retrieve':
            # TODO Ticket: #794
            return True
        elif view.action in ['update', 'partial_update']:
            # TODO Ticket: #792
            return True
        elif view.action == 'destroy':
            if request.user.is_superuser:
                return True

            # As all worflowlevel1 objects associated to an indicator have the
            # same org, we take the first one.
            organization = obj.workflowlevel1.first().organization
            is_org_admin = WorkflowTeam.objects.filter(
                workflow_user=request.user.tola_user,
                partner_org=organization,
                role__name=ROLE_ORGANIZATION_ADMIN).exists()
            if is_org_admin:
                return True

            is_program_admin = WorkflowTeam.objects.filter(
                workflow_user=request.user.tola_user,
                workflowlevel1__in=obj.workflowlevel1.all(),
                role__name=ROLE_PROGRAM_ADMIN).exists()
            if is_program_admin:
                return True

            return False
        else:
            return False
