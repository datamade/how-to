from django.core.management import call_command
import pytest


@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('load_cms_content')
