import pytest
import functools


@pytest.fixture
def client(client):
    """We enforce SSL in production (see settings.py) so test clients
    must also use SSL to work properly."""
    client.get = functools.partial(client.get, secure=True)
    client.post = functools.partial(client.post, secure=True)
    return client


# Define test fixtures here.
