from django_extensions.management.jobs import BaseJob
from django.core.management import call_command


class SearchJob(BaseJob):
    help = "Search index update job."

    def execute(self):
        # executing Search index update job
        call_command('search-index', '_all')

