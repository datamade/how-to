# 🔍 Searching Data, the DataMade way

1. [Lightweight](01-lightweight.md)
    - DataTables
    - django-filter
    - django-autocomplete-light
2. [Middleweight](02-middleweight.md)
    - Custom SQL (Postgres)
3. [Heavyweight](03-heavyweight.md)
   - Solr & Haystack
4. **Glossary**

## Glossary

**analyzers** – set of rules, or tokenizers and filters, specifying how to compare fields in an index and search terms issued to that index

**coalesce** – a [Postgres function](https://www.postgresql.org/docs/current/static/functions-conditional.html#FUNCTIONS-COALESCE-NVL-IFNULL) that returns its first non-null argument; useful for assigning default values, when retrieved data might be null. Related to: `to_tsvector` in Postgres

**corpus** – a body of entities for searching

**faceting** – sorting search results into categories; a kind of group by operation for search

**filters** – rules for transforming text before it is tokenized, or broken into pieces for comparison, e.g., remove punctuation, downcasing, etc.

**fuzzy matching** – a search method that enables approximate matches between the query and data, as given a specified threshold. Related to: “Middleweight” option (Postgres), “Heavyweight” option (Solr, Haystack)

**highlighting** – visual indication of piece of search result that matches search term

**index** – an organized collection of data, similar to a psql database with field-based entities. Related to: “Heavyweight” option (Solr, Haystack)

**lexeme** – a unit of language that contains normalized representations of words, e.g., run, running, runs belong to the same lexeme. Related to: `to_tsvector` in Postgres

**search engine** – program that accepts a term and identifies matching documents in a specified corpus, e.g., a database or index

**token** – piece of text to be compared in a search operation

**tokenizers** – a single rule for generating pieces of text to be compared, i.e., tokens, from a broader field or search term, e.g., n characters match, common lexeme, etc.
