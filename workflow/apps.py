from django.apps import AppConfig


class WorkflowAppConfig(AppConfig):
    name = 'workflow'
    verbose_name = 'workflows'

    def ready(self):
        import workflow.signals  # noqa
