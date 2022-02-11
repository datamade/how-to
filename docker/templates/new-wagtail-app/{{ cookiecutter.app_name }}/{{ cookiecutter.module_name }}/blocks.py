from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.images.blocks import ImageChooserBlock


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()

    class Meta:
        icon = 'doc-full'


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    link = blocks.URLBlock()

    class Meta:
        icon = 'plus-inverse'


class CalloutBlock(blocks.StructBlock):
    paragraph = blocks.RichTextBlock()

    class Meta:
        icon = 'form'


class TableBlock(WagtailTableBlock):
    table = WagtailTableBlock()

    class Meta:
        template = '{{ cookiecutter.module_name }}/blocks/table.html'
        icon = 'table'
        label = 'Table'


class TeamMemberBlock(blocks.StructBlock):
    first_name = blocks.CharBlock()
    last_name = blocks.CharBlock()
    position = blocks.CharBlock()
    photo = ImageChooserBlock(required=False)
