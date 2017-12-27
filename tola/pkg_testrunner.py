from django.test.runner import DiscoverRunner
from django.conf import settings


class PackageTestSuiteRunner(DiscoverRunner):
    """
    Runs only tests that belong to INSTALLED_APPS.
    """
    def build_suite(self, *args, **kwargs):
        suite = super(PackageTestSuiteRunner, self).build_suite(*args, **kwargs)
        tests = []
        for case in suite:
            app_module = case.__class__.__module__
            add_tests_from_suite = False
            for app in settings.INSTALLED_APPS:
                if '{}.'.format(app) in app_module:
                    add_tests_from_suite = True
            if add_tests_from_suite:
                tests.append(case)

        suite._tests = tests
        return suite
