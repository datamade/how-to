# Recommendation of adoption: Wagtail

Based on our research, we recommend adopting Wagtail as DataMade's content management system for Django projects.

## Proof of concept and pilot

To date we have completed two pilot projects using Wagtail:

1. [LISC CDNA](https://github.com/datamade/lisc-cnda)
2. [Lugar Center Oversight Hearing Index](https://github.com/datamade/committee-oversight)

## Prerequisite skills

Wagtail is a CMS built for Django, which is already an integral part of the DataMade stack.

Before beginning a first Wagtail implementation, all developers should read [The Zen of Wagtail](https://docs.wagtail.io/en/v2.8/getting_started/the_zen_of_wagtail.html) to familiarize themselves with the guiding concepts.

## Maintenance outlook

Wagtail an open source tool created by [Torchbox](https://torchbox.com/), an agency based in the UK. It has an active global contributor community ("currently #1 on the list of open source Python CMSs measured by Github activity," according to their website) and a strict release cycle. It's used by Google, NASA, MIT, Mozilla and more. Exactly predicting the future of a product is impossible, but all signs indicate that Wagtail is a reliable choice.

In terms of DataMade maintenance of projects made with Wagtail, it will be important to choose a standard CMS toolkit and build expertise across the team to ensure that all Wagtail projects can be maintained without high onboarding costs. We believe that there will continue to be CMS needs in new projects that can be met with Wagtail, which will provide opportunity for widespread team investment.

## For further exploration

Though we've already had success with Wagtail in client work, the following areas warrant further exploration and documentation:

1. **Create a pattern for content import/export process and media storage**

    We should settle on a pattern for importing and exporting CMS content—this is helpful during development, and for new deployments of a site. For the Lugar project we have a management command for importing and a Docker command for exporting in the README; see [here](https://github.com/datamade/committee-oversight#initial-cms-content). This was successful, but debugging file storage was burdensome. For future projects Wagtail media uploads could be stored in S3, as detailed in [this blog post](https://wagtail.io/blog/amazon-s3-for-media-files/).

2. **Create more reusable class-based views in Wagtail**

    In the Lugar project we successfully implemented a [DetailPage model](https://github.com/datamade/committee-oversight/blob/master/committeeoversightapp/models.py#L482) to replicate the functionality of a [DetailView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/). We were generally pleased with this approach, as it allowed us to create detail views that both auto-populated data and allowed users to edit fields. This pattern could be extended to other Django [class-based views](https://ccbv.co.uk/) such as ListView. In the Lugar project, page creation was handled manually by the client. For future iterations of detail pages with different client needs, we may want to set up a system to automatically create a page for each record.

3. **Using Wagtail for data management**

    For the two projects in which DataMade has so far implemented Wagtail, users have not been able to change data related to Django models not originally created in Wagtail. For example, for the Lugar project there is a separate custom interface for entering data about individual hearings. However, there is support for editing any model through Wagtail’s [ModelAdmin](https://docs.wagtail.io/en/v2.8/reference/contrib/modeladmin/) module. For simple data management needs this could be very powerful and warrants further investigation. It could alleviate our need for custom data management tool development on some projects, and would mean users only have to learn to use one interface. See [this how-to issue](https://github.com/datamade/how-to/issues/35).

4. **Explore using Wagtail for non-Django sites**

    As Wagtail is a headless CMS, it’s possible to use it with frameworks other than Django. For example, [here is an example of the Wagtail team building a site with Gatsby](https://wagtail.io/blog/using-gatsby-wagtail-build-case-study/). This has not yet been successfully implemented at DataMade, and could be a good R&D thread to pull on sometime.
