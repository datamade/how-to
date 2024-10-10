from wagtail import blocks
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


class ParagraphBlock(blocks.StructBlock):
    paragraph = blocks.RichTextBlock()
    width = blocks.ChoiceBlock(
        choices=[
            ("col-md-12", "Full Width"),
            ("col-md-6", "Half Width"),
        ]
    )

    class Meta:
        icon = "doc-full"


class ImageLinkBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text="Alternate text to show if the image doesn’t load",
    )
    link = blocks.URLBlock()
    width = blocks.ChoiceBlock(
        choices=[
            ("col-md-12", "Full Width"),
            ("col-md-6", "Half Width"),
        ]
    )

    class Meta:
        icon = "image"
