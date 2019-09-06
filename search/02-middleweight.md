# 🔍 Searching Data, the DataMade way

1. [Lightweight](01-lightweight.md)
    - DataTables
    - django-filter
    - django-autocomplete-light
2. **Middleweight**
    - Custom SQL (Postgres)
3. [Heavyweight](03-heavyweight.md)
   - Solr & Haystack
4. [Glossary](glossary.md)

## Middleweight

Using DataTables or django-filters to build a queryset from distinct fields comes with limitations. What if you want tailor-made filters? Do you need fuzzy matching? How about field aggregation? Querying the database with custom SQL can maximize data gathering possibilities.

### Pros

[Out-of-the-box Postgres](https://www.postgresql.org/docs/10/static/textsearch-controls.html) offers flexible, suspiciously dexterous search functionality:

* You write the SQL. You control what does and does not get returned.
* Postgres can account for the search term and its variants. _How?_ `to_tsvector` converts the swaths of plain text in your database into “lexemes,” or normalized representations of words, e.g., run, running, runs belong to the same lexeme. The SQL query return entries whenever the query matches the lexemes.

And look, there’s another way! You can access your data without writing any SQL: the Django ORM provides [a handy wrapper around the Postgres full text search engine](https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/search/).

### Cons

Like anything with some complexity, this approach comes with “gotcha” moments:

* _If writing raw SQL_: A field in the search might return NULL. (This can be true when [joining tables](https://github.com/datamade/occrp-timeline-tool/blob/master/occrp/views.py#L259), and a column in the resultant data does not have any value.) `to_tsvector(NULL)` returns NULL, even if the other fields being converted to a `ts_vector` have data. The fix? [Add `coalesce`](https://www.postgresql.org/docs/current/static/functions-conditional.html#FUNCTIONS-COALESCE-NVL-IFNULL).
* _If using the Django ORM:_ The Django ORM can be useful for small data or single queries, but may not scale very well. For example, Django takes time to calculate the search vector. If your tool makes autocomplete suggestions (i.e., queries the database while the user types), then the rapid stream of queries can result in a sluggish app. A solution? [Add a search vector field to the model(s)](https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/search/#searchvectorfield) and directly query that field: this way, Django need not calculate the vector in the moment of querying.

Using raw SQL may require you to build some functionality-from-scratch, which can be time-consuming and may replicate work already done. If you sense, for instance, that you need a more complex faceted search, then read on about Solr. On the other hand, if you have a simple, small dataset, then consider DataTables as an option.

### Resources to get started

- [“Postgres full-text search is Good Enough!“](http://rachbelaid.com/postgres-full-text-search-is-good-enough/) – a thorough exploration of what Postgres can and cannot do.
- [Complete documentation of Postgres full-text search](https://www.postgresql.org/docs/current/static/textsearch.html) – especially consider sections [12.1](https://www.postgresql.org/docs/current/static/textsearch-intro.html) and [12.3](https://www.postgresql.org/docs/current/static/textsearch-controls.html)

Still wanting more? Just keep in mind these three things:

1. Know how to grab query data. Most likely, you’ll use a query parameter and the request context: [in Flask](http://flask.pocoo.org/docs/1.0/reqcontext/) or [in Django](https://docs.djangoproject.com/en/2.1/ref/request-response/).
2. Decide on a way to execute raw SQL in your Python app environment. For Django, you can [use the `connection` object](https://docs.djangoproject.com/en/2.1/topics/db/sql/#executing-custom-sql-directly), and for Flask, you can use [sqlalchemy and the `create_engine`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine) function (which instantiates a new instance of an engine for connecting to your database).
3. Remember to use a [context manager](http://book.pythontips.com/en/latest/context_managers.html#context-managers) when executing your query.

## Examples

**[Large Lots](https://github.com/datamade/large-lots/blob/master/lots_admin/views.py#L85) (Django)**

Users can execute full text searches of designated fields in the database (i.e., [name or ward number](https://github.com/datamade/large-lots/blob/master/lots_admin/views.py#L149)) and order or filter those results by a variety of parameters (e.g., step number, applicant last name).

**[OCCRP](https://github.com/datamade/occrp-timeline-tool/blob/master/occrp/views.py) (Flask)**

Users can execute [full text searches of designated fields](https://github.com/datamade/occrp-timeline-tool/blob/master/occrp/views.py#L257), order results, and [filter with facets](https://github.com/datamade/occrp-timeline-tool/blob/master/occrp/views.py#L206).
