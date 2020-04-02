# Comparisons to existing tools

Over the past year DataMade has employed two CMS platforms:

- [Django CMS](https://www.django-cms.org/en/) for [Neighborhood Opportunity Fund](https://github.com/datamade/neighborhood-fund)
- [Wagtail](https://wagtail.io/) for [LISC CDNA](https://github.com/datamade/lisc-cnda) and the [Lugar Center Oversight Index](datamade/committee-oversight: ⚖️ Committee oversight map coding project for the Lugar Center)


## Wagtail vs. Django CMS

Both Wagtail and Django CMS are built for use with Django, but we were surprised to learn that they ask developers to employ substantially different abstractions—the way the two CMSs structure their data across views and models is quite different.

To facilitate deeper and more equal knowledge of DataMade CMSs, and thus speed up development time and improve maintainability, we should pick a single CMS platform and systematize its use.

In our experience, Wagtail is both easier to set up for developers and easier to use for content managers.

- While Django CMS's large community-built plugin library initially looked promising, we found that both third-party and default plugins for basic functions, such as rich text boxes to allow users to input and style text, had confusing interfaces and were often buggy.
- In terms of user experience, we found that Wagtail's backend interface is easier for users to pick up. While Django CMS offers greater flexibility and encourages users to simply click on section of a page to change it, in practice this was overwhelming. In contrast, Wagtail intentionally separates page design from content management in a way that usefully restricts users from changing too many pieces of a page at once.
- Overall, we found the Wagtail documentation more robust and reliable.
