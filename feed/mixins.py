from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from tola.util import getCountry
from workflow.models import *


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class UserCountryMixin(object):

    def list(self, request):
        user_countries = getCountry(request.user)
        queryset = WorkflowLevel1.objects.all().filter(country__in=user_countries)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserOrgMixin(object):

    def get_user(self, request):
        user_org = TolaUser.objects.get(user=request.user).organization__id
        return user_org

