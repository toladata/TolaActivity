from rest_framework import permissions
from workflow.models import TolaUser
from tola.util import getLevel1


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
        return request.user and request.user.is_authenticated()

    def check_object_permission(self, user, obj):
        return (user and user.is_authenticated() and
          (user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)


class UserIsTeamOrOrgAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        return request.user and request.user.is_authenticated()

    def check_object_permission(self, user, obj):
        return (user and user.is_authenticated() and
          (user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):

        user_level1 = getLevel1(request.user)
        user_org = TolaUser.objects.get(user=request.user).organization
        if view.action == 'list':
            return request.user.is_authenticated() and (obj in user_level1 and obj.organization in user_org
                                                or 'OrgAdmin' in request.user.groups.values_list('name', flat=True))
        if view.action == 'retrieve':
            return request.user.is_authenticated() and (obj in user_level1
                                                or 'OrgAdmin' in request.user.groups.values_list('name', flat=True))
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and (obj in user_level1
                                                or 'OrgAdmin' in request.user.groups.values_list('name', flat=True))
        elif view.action == 'destroy':
            return request.user.is_staff and 'OrgAdmin' in request.user.groups.values_list('name', flat=True)
        else:
            return False
