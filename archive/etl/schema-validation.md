# 🧩 Schema validation

Schema validation is a means of ensuring that incoming data matches an expected format. There are two primary components: definition and validation.

At DataMade, our preferred framework for schema validation is [`marshmallow`](https://marshmallow.readthedocs.io/en/stable/index.html).

### Contents

- [Getting started](#getting-started)
- [Examples](#examples)
- [Research](#research)
    - [Areas of further research](#areas-of-further-research)

## Getting started

`marshmallow` provides fairly extensive documentation. See [their quickstart](https://marshmallow.readthedocs.io/en/stable/quickstart.html) to get up and running quickly. For more advanced or specific development, see the relevant section of [their user guide](https://marshmallow.readthedocs.io/en/stable/index.html#guide).

## Examples

- University of Minnesota Elections Archive: [Definition](https://github.com/datamade/mn-election-archive/blob/7d6142a6bfea48527afa214e4c713195511b0503/elections/schemas.py) | [Validation](https://github.com/datamade/mn-election-archive/blob/7d6142a6bfea48527afa214e4c713195511b0503/elections/management/commands/transform.py)
- Dedupe.io API: Access to the Dedupe.io repository is limited to Dedupe.io developers. The schemas for API requests pre-process, authenticate, validate, and post-process data using `marshmallow`. If you wish to see an example of any or all of the above, request a gist of the relevant code [from a member of the `dedupeio` organization](https://github.com/orgs/dedupeio/people).

## Research

_Excerpted from a July 2019 implementation plan for the Dedupe.io API._

It would be ideal to lean on an existing schema validation library, rather than rolling our own solution, to reduce the amount of custom infrastructure we need to maintain. I propose using marshmallow, "a… library for converting complex data types, such as objects, to and from native Python data types." The documentation contains [a compelling section on its benefits](https://marshmallow.readthedocs.io/en/3.0/why.html) over other schema validation libraries.

Personally, I like:

* The ability to define schemas as Python classes
* Sensical and elegant interface (decorators) for custom, callable validators
* Returns all validation errors at once, enabling a nicer user experience with the API
* [Pre- and post-processing hooks](https://marshmallow.readthedocs.io/en/3.0/extending.html) for transforming valid data

I also considered:

* [jsonschema](https://github.com/Julian/jsonschema)
  * Pros
    * Familiar from applications in pupa and IHS
    * [Supports custom validation](https://lat.sk/2017/03/custom-json-schema-type-validator-format-python/)
  * Cons
    * Define schemas as dictionaries, not classes
    * Validation API is wonky
    * Does not support transformation
* [schema](https://github.com/keleshev/schema)
  * Pros
    * Seems to offer a lot of the same functionality as marshmallow
  * Cons
    * The API is inelegant

### Areas of further research

We like [Django REST framework](https://www.django-rest-framework.org/) for API development. It provides its own module for definiting and validating schemas, which we've used in a number of projects, however [there is a `django-rest-marshmallow` plugin](https://github.com/marshmallow-code/django-rest-marshmallow) that would allow us to use `marshmallow` serializers instead. It would be ideal to trial this in our next Django REST project, in order to more fully standardize our tooling for schema-related operations.
