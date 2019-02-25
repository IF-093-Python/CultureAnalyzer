from django.test.runner import DiscoverRunner
from django.core.management import call_command


class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        databases = super().setup_databases(**kwargs)
        call_command("loaddata", "users/fixtures/fixtures.json")
        return databases
