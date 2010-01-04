from django.core.management.base import BaseCommand
from xmms2_django.daemon import daemon


class Command(BaseCommand):
    def handle(self, *args, **options):
        daemon.main(args)
