from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.panels import FieldPanel

from {{cookiecutter.module_name}}.blocks import (
    AccordionBlock,
    ButtonBlock,
    CalloutBlock,
    TableBlock,
    TeamMemberBlock,
    ParagraphBlock,
    ImageLinkBlock,
)
from {{ cookiecutter.module_name }}.utils import get_site_menu


class BasePage(Page):
    body = StreamField(
        [
            ("paragraph", ParagraphBlock()),
            ("heading", blocks.CharBlock(classname="full title", icon="title")),
            ("accordion", blocks.ListBlock(AccordionBlock(), icon="list-ul")),
            ("button", ButtonBlock()),
            ("image_link", ImageLinkBlock()),
            ("callout", CalloutBlock()),
            ("table", TableBlock()),
            (
                "embedded_media",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=False)),
                        ("media_link", EmbedBlock()),
                        ("description", blocks.TextBlock(required=False)),
                    ],
                    icon="media",
                ),
            ),
            ("team_members", blocks.ListBlock(TeamMemberBlock(), icon="group")),
        ]
    )

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["menu"] = get_site_menu()
        return context

    class Meta:
        abstract = True



class StaticPage(BasePage):
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['{{ cookiecutter.module_name }}.HomePage']


class HomePage(BasePage):
    intro_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        FieldPanel('body')
    ]

    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)

        return context
