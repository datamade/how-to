from django.conf import settings


def base_context(request):
    return {
        'allow_index': settings.ALLOW_SEARCH_INDEXING
    }
