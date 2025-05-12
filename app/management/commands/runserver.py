from django.core.management.commands.runserver import Command as RunserverCommand
from django.conf import settings

class Command(RunserverCommand):
    def handle(self, *args, **options):
        options['port'] = getattr(settings, 'PORT', 8001)
        super().handle(*args, **options)
