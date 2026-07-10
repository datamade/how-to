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

Do you need more control of fuzzy matches than Postgres search vectors provide? Do calculated values slow your queries to a crawl? Is your search corpus just plain huge? While a more involved solution than issuing SQL or handling search client side, an implementation of powerful search engine [ElasticSearch](https://www.elastic.co/) may be your best bet.

If you’re implementing search for a Django application, [Haystack](https://django-haystack.readthedocs.io/en/master/tutorial.html) is an extension that connects your application to a custom search engine, e.g., ElasticSearch. While it’s not without pitfalls, Haystack provides a familiar API for defining your search fields, issuing queries, and retrieving results and so can smooth your transition to a more complex search setup. 

You should under no circumstances write custom adapter code to interact with ElasticSearch. You will end up reimplementing much of HayStack badly.

Beware: Configuring and administering ElasticSearch is of intermediate to advanced difficulty. When you need a fancy search, however, it can be well worth the effort (and we have some experienced hands on deck who are happy to help).

### Pros

* HayStack is infinitely configurable.
* You control [how your data and queries are broken apart and compared](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html) via analyzers, tokenizers, and filters.
* [Faceting](https://www.elastic.co/guide/en/app-search/current/facets-guide.html), [auto-suggest](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html), [geosearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html): ElasticSearch does it all.
* Excellent [documentation](https://www.elastic.co/guide/index.html).

### Cons

* ElasticSearch is infinitely configurable.
* ElasticSearch process must be managed separately from your application, though this is made less of a problem with containerization (e.g., Docker). 

### Getting started

#### Run ElasticSearch

1. Create a `docker-compose.yml` file at the root of your project directory.


```yaml
  elasticsearch:
    image: elasticsearch:7.14.2
    container_name: chi-councilmatic-elasticsearch
    ports:
      - 9200:9200
    environment:
      - discovery.type=single-node
      - logger.org.elasticsearch.discovery=DEBUG
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    mem_limit: 1g
    volumes:
      - yourapp-es-data:/usr/share/elasticsearch/data

    volumes:
      yourapp-es-data:
```

## Examples

**chi-councilmatic (Django)**

Query large bodies of text. Return faceted & highlighted results.

* [Haystack index](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/haystack_indexes.py) and [custom text-rendering template](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/templates/search/indexes/councilmatic_core/bill_text.txt)
* [Search form](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/views.py#L95) and [search view](https://github.com/datamade/django-councilmatic/blob/e61e5215e2dc24937643dcb9f68a8266b00275e2/councilmatic_core/views.py#L39)
