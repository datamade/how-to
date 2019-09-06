# 🔍 Searching Data, the DataMade way

1. [Lightweight](01-lightweight.md)
    - DataTables
    - django-filter
    - django-autocomplete-light
2. [Middleweight](02-middleweight.md)
    - Custom SQL (Postgres)
3. **Heavyweight**
   - Solr & Haystack
4. [Glossary](glossary.md)

## Heavyweight

Do you need more control of fuzzy matches than Postgres search vectors provide? Do calculated values slow your queries to a crawl? Is your search corpus just plain huge? While a more involved solution than issuing SQL or handling search client side, an implementation of powerful search engine [Solr](https://lucene.apache.org/solr/guide/7_1/index.html) may be your best bet.

If you’re implementing search for a Django application, [Haystack](https://django-haystack.readthedocs.io/en/master/tutorial.html) is an extension that connects your application to a custom search engine, e.g., Solr. While it’s not without pitfalls, Haystack provides a familiar API for defining your search fields, issuing queries, and retrieving results and so can smooth your transition to a more complex search setup.

Beware: Configuring and administering Solr is of intermediate to advanced difficulty. When you need a fancy search, however, it can be well worth the effort (and we have some experienced hands on deck who are happy to help).

### Pros

* Solr is infinitely configurable.
* You control [how your data and queries are broken apart and compared](https://lucene.apache.org/solr/guide/7_1/understanding-analyzers-tokenizers-and-filters.html) via analyzers, tokenizers, and filters.
* Handy dandy web GUI for testing [query analysis](https://lucene.apache.org/solr/guide/7_1/analysis-screen.html#analysis-screen), [results](https://lucene.apache.org/solr/guide/7_1/query-screen.html), and more.
* [Faceting](https://lucene.apache.org/solr/guide/7_1/faceting.html), [highlighting](https://lucene.apache.org/solr/guide/7_1/highlighting.html), [auto-suggest](https://lucene.apache.org/solr/guide/7_1/suggester.html), [geosearch](https://lucene.apache.org/solr/guide/7_1/spatial-search.html): Solr does it all.
* Excellent [documentation](https://lucene.apache.org/solr/guide/7_1/index.html).

### Cons

* Solr is infinitely configurable.
* Solr provides a powerful engine; you have to handle the results yourself.
* Solr process must be managed separately from your application, though this is made less of a problem with containerization (e.g., Docker).
* There are some non-obvious pitfalls and equally non-obvious solutions, e.g., [“deep paging” (read: going more than a few pages into search results) is inefficient](https://lucene.apache.org/solr/guide/7_1/pagination-of-results.html#performance-problems-with-deep-paging) but can be mitigated with [cursor marks](https://lucene.apache.org/solr/guide/7_1/pagination-of-results.html#fetching-a-large-number-of-sorted-results-cursors).
* Haystack can help or hinder, depending on your use case. As with any library, you trade the convenience of using someone else’s work for the idiosyncrasies of their implementation. For example, it inexplicably gobbles memory while building the Solr index. We’re [working on a solution](https://github.com/datamade/django-councilmatic/pull/219) for this particular quirk, but there are [other head scratchers](https://django-haystack.readthedocs.io/en/master/searchqueryset_api.html?highlight=%22hl.fl%22#SearchQuerySet.highlight) to overcome.

### Getting started

#### Run Solr

1. Copy solr_configs directory to your project. Here’s [a pretty basic one](https://github.com/datamade/bga-payroll/tree/master/solr_configs).

2. Create a `docker-compose.yml` file at the root of your project directory.


    ```yaml
    version: '2.4'

    services:
      solr:
        image: solr:latest
        container_name: <APP_NAME>-solr
        volumes:
          - ./solr_configs:/<APP_NAME>_configs
          - solr-data:/opt/solr/server/solr/mycores
        command: sh -c 'solr-create -c <SOLR_CORE_NAME> -d /<APP_NAME>_configs'
        ports:
          - 8986:8983
        environment:
          SOLR_LOG_LEVEL: INFO
        restart: on-failure

    volumes:
      solr-data:
    ```

    Next, in your terminal, run `docker-compose up -d solr`. To view the logs, run `docker logs -f solr`. To stop Solr, or if you make changes to your underlying Solr or container configuration, run `docker-compose down`. This will remove your Solr container, but keep your index data in tact, thanks to use of the named `solr-data` volume. To spin up a new Solr container, start over with `docker-compose up -d solr`.

#### Configure Haystack

The [Haystack docs](https://django-haystack.readthedocs.io/en/master/tutorial.html#getting-started-with-haystack) give a clear, step-by-step guide for Solr-Django integration. The basic steps entail the following.

1. Tell your Django app where Haystack can find Solr (i.e., define a [HAYSTACK_CONNECTIONS](https://django-haystack.readthedocs.io/en/master/tutorial.html#solr) variable in your settings).
2. Create a [Haystack SearchIndex](https://django-haystack.readthedocs.io/en/master/tutorial.html#handling-data). Define the models to be indexed in a *.py file, as with [django-councilmatic](https://github.com/datamade/django-councilmatic/blob/master/councilmatic_core/haystack_indexes.py).
3. Run build_solr_schema & update_index [management commands](https://django-haystack.readthedocs.io/en/master/management_commands.html).
    - Building an index can consume substantive memory, and Haystack does not have great memory management. Call these commands with a batch size argument to avoid memory errors, e.g., `python manage.py rebuild_index --batch-size=100`.
4. Use a Haystack [search view](https://django-haystack.readthedocs.io/en/master/views_and_forms.html#views) and [search form](https://django-haystack.readthedocs.io/en/master/views_and_forms.html#forms) to query your new index.

### Examples

**django-councilmatic (Django)**

Query large bodies of text. Return faceted & highlighted results.

* [Haystack index](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/haystack_indexes.py) and [custom text-rendering template](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/templates/search/indexes/councilmatic_core/bill_text.txt)
* [Search form](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/views.py#L95) and [search view](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/views.py#L39)

**nyc-council-councilmatic (Django, extends django-councilmatic)**

Ditto django-councilmatic, but makes it _custom_.

* [Haystack index](https://github.com/datamade/nyc-council-councilmatic/blob/94974de317e34dcb05165a7c23717960c400d942/nyc/search_indexes.py) and [custom text-rendering template](https://github.com/datamade/nyc-council-councilmatic/blob/94974de317e34dcb05165a7c23717960c400d942/nyc/templates/search/indexes/nyc/bill_text.txt)
* [Search view](https://github.com/datamade/nyc-council-councilmatic/blob/94974de317e34dcb05165a7c23717960c400d942/nyc/views.py#L213)

**la-metro-councilmatic (Django, extends django-councilmatic)**

Ditto django-councilmatic, but makes it _custom_. Notable for its implementation of a custom Haystack Highlighter class, which allows for exact multi-word matching.

* [Custom Highlighter](https://github.com/datamade/django-councilmatic/blob/master/councilmatic_core/utils.py) in django-councilmatic
* [Simple tag](https://github.com/datamade/la-metro-councilmatic/blob/84d0e9c5c954dcc262bce33fd98a4ac58c2f9501/lametro/templatetags/lametro_extras.py#L196) and [the rendering of search results](https://github.com/datamade/la-metro-councilmatic/blob/84d0e9c5c954dcc262bce33fd98a4ac58c2f9501/lametro/templates/partials/search_result.html#L22)
