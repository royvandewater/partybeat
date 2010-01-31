from django.core.management.base import BaseCommand
from partybeat.daemon import daemon


class Command(BaseCommand):
    def handle(self, *args, **options):
        daemon.main(args)
