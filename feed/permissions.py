from django.contrib.auth.models import Group
from rest_framework import permissions

from tola.util import getLevel1
from workflow.models import (
    TolaUser, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN, WorkflowTeam)


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
            return (request.user.is_authenticated() and
                    (obj in user_level1 and obj.organization in user_org
                     or ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list('name', flat=True)))
        if view.action == 'retrieve':
            return (request.user.is_authenticated() and
                    (obj in user_level1 or
                     ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list('name', flat=True)))
        elif view.action in ['update', 'partial_update']:
            return (request.user.is_authenticated() and
                    (obj in user_level1 or
                     ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list('name', flat=True)))
        elif view.action == 'destroy':
            if request.user.is_superuser:
                return True
            elif ROLE_ORGANIZATION_ADMIN in request.user.groups.values_list('name', flat=True):
                return True

            group_program_admin = Group.objects.get(name=ROLE_PROGRAM_ADMIN)
            try:
                WorkflowTeam.objects.get(workflow_user=request.user.tola_user, workflowlevel1=obj,
                                         role=group_program_admin)
            except WorkflowTeam.DoesNotExist:
                return False
            else:
                return True
        else:
            return False
