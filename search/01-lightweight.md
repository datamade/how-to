# 🔍 Searching Data, the DataMade way

1. **Lightweight**
    - DataTables
    - django-filter
    - django-autocomplete-light
2. [Middleweight](02-middleweight.md)
    - Custom SQL (Postgres)
3. [Heavyweight](03-heavyweight.md)
   - Solr & Haystack
4. [Glossary](glossary.md)

## Lightweight

If you’re directly searching just a few fields in your data and want to get up and running fast, consider one of the following.

### DataTables

[DataTables](https://datatables.net/) converts your HTML tables into interactive tables that are searchable by any field. It also has neat options like prebuilt PDF and CSV [download buttons](https://datatables.net/extensions/buttons/examples/initialisation/export.html), automatic [pagination](https://datatables.net/reference/option/paging), and integration with [Bootstrap](https://datatables.net/examples/styling/bootstrap4).

To get started, follow DataTables’ [installation guide](https://datatables.net/manual/installation).

ADD: Django Server-side Data Tables

DataTables is simple to set up and gets your search off the ground fast. However, it limits your options in both functionality and design and doesn’t always work well with mobile.

### django-filter

[django-filter](https://django-filter.readthedocs.io/en/master/) is a nifty Django application that helps you filter a queryset by a model’s fields. You’ll write a `filters.py` file that generates a Django form. ([Helpful blog post](https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html).)

Django-filter can be used in conjunction with [Select2](https://select2.org/) for prettier selection boxes, and with [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for more fine-grained form styling.

### django-autocomplete-light

#### In the admin interface

If you require autocomplete search in the admin interface and you’re using Django 2.0 or above, the Django ModelAdmin object has an [autocomplete_fields](https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields) attribute that converts the specified attributes to Select2 autocomplete fields, no other steps or external libraries required. (If you aren’t using Django 2.0 or above, read up on django-autocomplete-light in “In the user interface,” below.)

This is a great option if you need something that Just Works.™ While there are some facilities for making this option your own, YMMV for custom behavior.

#### In the user interface

For your user-facing needs, [django-autocomplete-light](https://django-autocomplete-light.readthedocs.io/en/master/index.html) provides a useful set of utilities for rendering a Select2 autocomplete widget. To use it, simply:

* [Set up a view](https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#create-an-autocomplete-view) to return the appropriate queryset, given a search term.
* [Create a form](https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#use-the-view-in-a-form-widget) with an autocomplete field.
* Render the form in a template, [being sure to include {{ form.media }}](https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#using-autocompletes-outside-the-admin) (i.e., the appropriate JavaScript files).

Greater detail, as well as examples, can be found in [this handy tutorial](https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html).

On the plus side, Select2 is already integrated into this option, i.e., you don’t need to set it up separately. Additionally, unlike DataTables, django-autocomplete-light goes beyond data display, so it comes in handy when you want to use the selection to do something other than filter data.

On the other hand, there are multiple moving parts to getting django-autocomplete-light up and running. If you find yourself setting up an autocomplete view that does no additional filtering just for search, falling back to DataTables may just as effective, in half the time.

### Examples

**[SSCE Dashboard](https://github.com/datamade/cps-ssce-dashboard) (Django)**

Users can search by school name on the landing page, a simple table made [searchable](https://github.com/datamade/cps-ssce-dashboard/blob/master/cps_app/templates/cps_app/search.html#L123) with DataTables. The [filters](https://github.com/datamade/cps-ssce-dashboard/blob/master/cps_app/filters.py) use django-filter.

**[Councilmatic](https://github.com/datamade/la-metro-councilmatic/blob/master/lametro/templates/lametro/board_members.html#L165)** **(Django)**

The council members view page includes a basic data table.

**DePaul IHS Website ([1](https://github.com/datamade/ihs-website-v2/blob/34966e62612b96c18235e46adf6d11d0d465548e/templates/dataportal/datatables_index.html#L383), [2](https://github.com/datamade/ihs-website-v2/blob/34966e62612b96c18235e46adf6d11d0d465548e/templates/dataportal/datatables_index.html#L383)) (Django)**

The data portal includes multiple, toggle-able data tables on the same page, with fixed headers and footers, and responsive data display.

**[BGA Payroll Database](https://github.com/datamade/bga-payroll/blob/9de0f4c02fde86038ee109288ab663d64c7fdf7b/data_import/admin.py) (Django)**

Add a responding agency autocomplete field to the admin interface for uploading source files. Customize the options displayed in the autocomplete by overriding the `get_search_results` method of the responding agency ModelAdmin.

ADD: Link to Lugar (server-side data tables)
