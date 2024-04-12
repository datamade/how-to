# Using Django Rest Framework serializers for data serialization
Django Rest Framework can be useful for serializing data beyond the context of an API endpoint. We find it helpful whenever we're serializing json for use in a React component, like when you need to pass GeoJSON to a map or your data objects have nested relationships.

[DRF's docs](https://www.django-rest-framework.org/api-guide/serializers/) are the best place to learn about the serializer classes, but this document has examples for how we use this pattern within the DataMade stack.

## Use cases
- Serializing GeoJSON or JSON data for use in a Django template or React component that's [baked into the Django template](/django/django-react-integration.md)
- Serializing a queryset with nested relationships
  -  This helps with database efficiency because you can leverage `prefetch_related` and then serialize all of the related data in a cleaner way. [This blog post is a good resource to learn about that](https://hakibenita.com/django-rest-framework-slow).


## Examples:
In the IL NWSS project, we serialized GeoJSON data and linked needed data that is related to the model. I can't share the private repo link since not everybody has access, so these are the relevant changes we made:

### models.py
```python
from django.contrib.gis.db import models'


class SewershedArea(models.Model):
    """Simplified version of the geo model"""
    treatment_plant = ParentalKey(
        WastewaterTreatmentPlant,
        related_name='sewershed_area',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    boundary = models.GeometryField(blank=True, null=True, srid=3435, dim=2)

```

### serializers.py
```python
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer,
    GeometrySerializerMethodField,
)


class SewershedAreaGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SewershedArea
        fields = ('pk', 'boundary', 'plant_name', 'plant_url', 'plant_city', 'site_id')
        geo_field = 'boundary'
    
    boundary = GeometrySerializerMethodField()

    plant_name = serializers.SerializerMethodField()
    plant_url = serializers.SerializerMethodField()
    plant_city = serializers.SerializerMethodField()
    site_id = serializers.SerializerMethodField()

    def get_boundary(self, obj):
        return obj.boundary.transform(4326, clone=True)

    def get_plant_name(self, obj):
        return obj.treatment_plant.name

    def get_plant_url(self, obj):
        return obj.treatment_plant.get_absolute_url()

    def get_plant_city(self, obj):
        return obj.treatment_plant.city

    def get_site_id(self, obj):
        return obj.treatment_plant.site_id

    
```

### Use the data
You can use the serialized data in at least two ways:
1. Serialize the GeoJSON data in your view and pass it into the context, so that you can access that data within the template and pass it into your React component as props (as described in [this how-to documentation](/django/django-react-integration.md#set-react-props-and-root-element-on-the-window-object))

2. Setup an API endpoint with Django Rest Framework
