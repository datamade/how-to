from django.utils.html import escape
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler


@hooks.register('register_rich_text_features')
def register_blockquote_feature(features):

    feature_name = 'blockquote'
    feature_type = 'blockquote'
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature({
            'type': feature_type,
            'label': '"',
            'description': 'Blockquote',
            'element': 'blockquote'
        })
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'blockquote': BlockElementHandler(feature_type)
        },
        'to_database_format': {
            'block_map': {
                feature_type: 'blockquote'
            }
        }
    })
    features.default_features.append('blockquote')


class NewWindowExternalLinkHandler(LinkHandler):
    # This specifies to do this override for external links only.
    # Other identifiers are available for other types of links.
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        # Let's add the target attr, and also rel="noopener" + noreferrer fallback.
        # See https://github.com/whatwg/html/issues/4078.
        return '<a href="%s" target="_blank" rel="noopener noreferrer">' % escape(href)


@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NewWindowExternalLinkHandler)
