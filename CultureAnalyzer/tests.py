from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        databases = super().setup_databases(**kwargs)
        return databases
