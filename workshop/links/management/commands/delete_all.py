import argparse

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from links.models import Link, Tag, LinkTag


class Command(BaseCommand):
    help = 'Load data from a file'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for link in Link.objects.all():
            link.delete()
        for tag in Tag.objects.all():
            tag.delete()
        self.stdout.write(self.style.SUCCESS('Todo ok'))
