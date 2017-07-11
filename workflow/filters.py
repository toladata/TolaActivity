import django_filters
from models import WorkflowLevel2
from rest_framework.filters import DjangoFilterBackend


class AllDjangoFilterBackend(DjangoFilterBackend):
    """
    A filter backend that uses django-filter.
    """

    def get_filter_class(self, view, queryset=None):
        """
        Return the django-filters `FilterSet` used to filter the queryset.
        """

        class AutoFilterSet(self.default_filter_set):
            class Meta:
                model = queryset.model
                fields = None

        return AutoFilterSet


class ProjectAgreementFilter(django_filters.FilterSet):

    class Meta:
        model = WorkflowLevel2
        fields = ['activity_code', 'project_name', 'beneficiary_type','workflowlevel1','sector']

    def __init__(self, *args, **kwargs):
        super(ProjectAgreementFilter, self).__init__(*args, **kwargs)
