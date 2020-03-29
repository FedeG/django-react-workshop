import argparse

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from links.models import Link, Tag, LinkTag


class Command(BaseCommand):
    help = 'Load data from a file'

    def add_arguments(self, parser):
        parser.add_argument('stars', type=int)
        parser.add_argument('username', type=str)
        parser.add_argument('file', type=argparse.FileType('r'))

    def load_link(self, user, url, stars, tag):
        try:
            link = Link.objects.create(
                stars=stars,
                user=user,
                url=url
            )
            link.save()
            self.links += 1
        except IntegrityError:
            link = Link.objects.get(url=url)
            self.links_r += 1
        self.create_link_tag(link, tag)

    def create_link_tag(self, link, tag):
        try:
            link_tag = LinkTag.objects.create(link=link, tag=tag)
            link_tag.save()
            self.link_tags += 1
        except IntegrityError:
            self.link_tags_r += 1

    def load_tag(self, user, tag_name):
        try:
            tag = Tag.objects.create(
                name=tag_name,
                user=user,
            )
            tag.save()
            self.tags += 1
            self.stdout.write(self.style.SUCCESS('Add TAG: {}'.format(tag.name)))
        except IntegrityError:
            tag = Tag.objects.get(name=tag_name)
            self.tags_r += 1
        return tag

    def handle(self, *args, **options):
        self.links = 0
        self.tags = 0
        self.link_tags = 0
        self.links_r = 0
        self.tags_r = 0
        self.link_tags_r = 0
        user = User.objects.get(username=options['username'])
        tag = Tag.objects.get(name='Sin Tag')
        with options['file'] as file_with_links:
            for _, line in enumerate(file_with_links):
                if line[0] == '#' or line[0] == '%':
                    tag_name = line.split('#')[-1].split('%')[-1].strip()
                    tag = self.load_tag(user, tag_name)
                elif len(line) > 5:
                    url = line.strip()
                    self.load_link(user, url, options['stars'], tag)
                self.stdout.write(
                    self.style.SUCCESS('Status: L {} Lr {} T {} Tr {} LT {} LTr {}'.format(
                        self.links,
                        self.links_r,
                        self.tags,
                        self.tags_r,
                        self.link_tags,
                        self.link_tags_r
                    ))
                )
        self.stdout.write(self.style.SUCCESS('Todo ok'))
