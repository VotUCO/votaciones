from django.test.runner import DiscoverRunner
from django.core.management import call_command

class MigrationTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Configurar las bases de datos (crear y configurar la base de datos de test)
        result = super().setup_databases(**kwargs)
        # Forzar la ejecución de las migraciones
        call_command('makemigrations', verbosity=1, interactive=False)
        call_command('migrate', verbosity=1, interactive=False)
        return result