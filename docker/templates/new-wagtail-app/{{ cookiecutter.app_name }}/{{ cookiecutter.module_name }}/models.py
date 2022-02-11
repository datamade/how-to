from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel

from {{cookiecutter.module_name}}.blocks import AccordionBlock, ButtonBlock, CalloutBlock, TableBlock, \
    TeamMemberBlock


class BasePage(Page):
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock(classname='full title', icon='title')),
        ('accordion', blocks.ListBlock(AccordionBlock(), icon='list-ul')),
        ('button', ButtonBlock()),
        ('callout', CalloutBlock()),
        ('table', TableBlock()),
        ('embedded_media', blocks.StructBlock([
            ('title', blocks.CharBlock(required=False)),
            ('media_link', EmbedBlock()),
            ('description', blocks.TextBlock(required=False))
        ], icon='media')),
        ('team_members', blocks.ListBlock(TeamMemberBlock(), icon='group')),
    ])

    class Meta:
        abstract = True


class StaticPage(BasePage):
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['{{ cookiecutter.module_name }}.HomePage']


class HomePage(BasePage):
    intro_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text'),
        StreamFieldPanel('body')
    ]

    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)

        return context
