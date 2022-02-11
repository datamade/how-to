from wagtail.images.formats import Format, register_image_format,\
  unregister_image_format

unregister_image_format('fullwidth')
register_image_format(Format('fullwidth',
                             'Full width',
                             'richtext-image img-fluid mx-auto d-block',
                             'width-1000'))

unregister_image_format('left')
register_image_format(Format('left',
                             'Left-aligned',
                             'richtext-image float-left img-fluid',
                             'width-500'))

unregister_image_format('right')
register_image_format(Format('right',
                             'Right-aligned',
                             'richtext-image float-right img-fluid',
                             'width-500'))
