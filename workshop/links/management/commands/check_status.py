import grequests
from requests.exceptions import MissingSchema

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from links.models import Link


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


class Command(BaseCommand):
    help = 'Check online status'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        online_links = 0
        offline_links = 0
        errors = 0
        total = 0

        links = Link.objects.filter(status=Link.CHECK)
        size = links.count() // 30
        chunks = chunker_list(links, size)
        for chunk_links in chunks:
            rs = (grequests.get(link.url) for link in chunk_links)
            total += 30
            for index, response in enumerate(grequests.map(rs)):
                link = chunk_links[index]
                if response is None:
                    link.status = Link.ERROR
                    errors += 1
                    self.stdout.write('Error en la url {}'.format(link.url))
                elif response.status_code == 200:
                    link.status = Link.ONLINE
                    online_links += 1
                else:
                    link.status = Link.OFFLINE
                    offline_links += 1
                link.save()
                self.stdout.write(
                    self.style.SUCCESS('Status ({}/{}): ON {} OFF {} ERR {}'.format(
                        total,
                        len(links),
                        online_links,
                        offline_links,
                        errors
                    ))
                )
        self.stdout.write(self.style.SUCCESS('Todo ok'))
