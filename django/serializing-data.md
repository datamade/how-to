# Using Django Rest Framework serializers for data serialization
Django Rest Framework can be useful for serializing data beyond the context of an API endpoint. We find it helpful whenever we're serializing json for use in a React component, like when you need to pass GeoJSON to a map or your data objects have nested relationships.

DRF's docs are the best place to learn about the serializer classes, but this document points you to see how we use this pattern within the DataMade stack.

## Use cases
- Serializing GeoJSON or JSON data for use in a Django template or React component that's [baked into the Django template](/django/django-react-integration.md)
- Serializing a queryset with nested relationships
  -  This helps with database efficiency because you can leverage `prefetch_related` and then serialize all of the related data in a cleaner way. [This blog post is a good resource to learn about that](https://hakibenita.com/django-rest-framework-slow).


## DataMade Examples:
1. **IL NWSS app**: We [serialized GeoJSON data and linked the data is linked to model](https://github.com/illinoisdpi/il-nwss-dashboard/pull/171).
2. **CCFP Asset Dashboard**: We had to [serialize GeoJSON with a readable and writeable API endpoint](https://github.com/fpdcc/ccfp-asset-dashboard/pull/106). Reading and writing with the GeoJSON serializers wasn't straightforward so this example might help somebody who needs to do that.
