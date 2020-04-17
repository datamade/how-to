# Comparisons to existing tools

Over the past year DataMade has employed four CMS platforms:

- [The Django admin site](https://docs.djangoproject.com/en/stable/ref/contrib/admin/) for [BGA Payroll](https://github.com/datamade/bga-payroll) and [BGA Pensions](https://github.com/datamade/bga-pensions)
- [`feincms3`](https://github.com/matthiask/feincms3) for the [IHS Website Redesign](https://github.com/datamade/ihs-website-v2)
- [Django CMS](https://www.django-cms.org/en/) for [Neighborhood Opportunity Fund](https://github.com/datamade/neighborhood-fund)
- [Wagtail](https://wagtail.io/) for [LISC CDNA](https://github.com/datamade/lisc-cnda) and the [Lugar Center Oversight Index](https://github.com/datamade/committee-oversight)

We discuss each of these in turn, below.

To facilitate deeper and more equal knowledge of CMS practices at DataMade, and
thus speed up development time and improve maintainability, we should pick a
single CMS tool and systematize its use.

Our pick is **Wagtail**, for the following reasons:

- Wagtail offers a superior developer experience, from installation to customization.
- Wagtail offers a superior user interface for a variety of content management tasks.
- Wagtail has robust and reliable documentation.
- Wagtail has a broad user base and [healthy plugin ecosystem](https://github.com/springload/awesome-wagtail).

### The Django admin site

The Django admin site comes with Django out of the box, and as such, it "just
works", no installation required. It is also reasonably well-documented, and
like the rest of the Django ecosystem, it has a healthy and helpful userbase,
making it easy to track down blog posts and StackOverflow threads for edge cases
and errors that aren't covered by the documentation.

Predictably, the Django admin interface offers a no-frills but functional interface
for managing Django models. It can also be extended fairly easily to support
custom admininstration tasks, such as flushing the cache.

However, for clients, who may be less intimately familiar with the underlying
data model, the Django admin site can be difficult to navigate, in particular
for applications that use highly normalized data. Moreover, the Django admin
site does not offer a rich text editor. For these reasons, we've had to compile
extensive documentation for client use of the Django admin site, with only
limited adoption in the long term.

### `feincms3`

`feincms3` is an extension of the Django admin interface that's optimized for
managing more complicated content hierarchies, e.g., nested pages. It has
[fairly complete documentation](https://feincms3.readthedocs.io/en/latest/index.html),
plus [a helpful example application](https://github.com/matthiask/feincms3-example),
however the developer experience is mixed. In particular, `feincms3` [implements
_only_ abstract classes and mixins](https://feincms3.readthedocs.io/en/latest/introduction.html),
so standing up an instance requires a certain familiarity with these concepts,
which isn't always true of newer developers.

The user interface is similar to the Django admin interface, with the added
ability to organize content in a tree editing interface. Unfortunately, this
interface is slightly confusing, and it doesn't always behave as expected.
`feincm3` also has an optional CKEditor integration, enabling rich text
editing, but the [documentation for `django-ckeditor`](https://github.com/django-ckeditor/django-ckeditor)
is sparse and configuration can be cryptic. Moreover, because CKEditor supports
so many kinds of content editing, none of them offer an excellent user
experience.

Unlike Wagtail and Django CMS, `feincms3` does not offer documentation for
content editors. For this reason, and because the user interface isn't terribly
straightforward, we've had to write especially detailed documentation for
clients to successfully manage content on their own.

### Django CMS

Wagtail and Django CMS are both built for use with Django, but they ask
developers to employ substantially different modes of thinking. The way the two
CMSs structure their data across views and models is quite different.

Django CMS operates with plugin-based abstractions, where pages are build from
discrete reusable units. It has some recommended default plugins, like a text
box and image field, and the ability to build and insert custom plugins.

While Django CMS's large community-built plugin library initially looked
promising, we found that both third-party and default plugins for basic
functions, such as rich text boxes to allow users to input and style text,
had confusing interfaces and were often buggy.

While Django CMS offers greater flexibility and encourages users to simply click
on section of a page to change it, in practice this was overwhelming. With so
much flexibility, plus the UI bugs outlined above, we've again needed to write
extensive documentation for clients.

### Wagtail

In our experience, Wagtail is easiest to set up for developers and easier to
use for content managers.

In terms of user experience, we found that Wagtail's backend interface is easier
for users to pick up. Wagtail intentionally separates page design from content
management in a way that usefully restricts users from changing too many pieces
of a page at once.

Wagtail relies on template-based abstractions. It encourages developers to write
reusable templates with different page layouts, and has a useful [StreamField](https://docs.wagtail.io/en/stable/topics/streamfield.html) model that allows some flexibility in pages built from the same template.
