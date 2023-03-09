# Adapted from https://github.com/rdegges/django-clear-cache
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    help = 'Fully clear your site-wide cache.'

    def handle(self, *args, **kwargs):
        try:
            assert settings.CACHES
        except AttributeError:
            raise CommandError(
                'No cache configured. Check CACHES in settings.py.'
            )

        cache.clear()
        self.stdout.write('Successfully cleared the cache.')
