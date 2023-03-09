# Django Compressor settings
from django.templatetags.static import static


STATICFILES_FINDERS = (
    *STATICFILES_FINDERS,
    "compressor.finders.CompressorFinder",
)

# This array determines which command django-compressor will run for each
# script type (<script type="module"> for vanilla JavaScript, <script
# type="text/jsx"> for React). CLI options are _combined_ with the options in
# the package Babel config, babel.config.json. By default, we use the
# @babel/preset-env preset. Need to transpile browser incompatible plugins?
# Add them to the "only" array in babel.config.json, as documented in the
# README under "Ensuring browser compatibility".
COMPRESS_PRECOMPILERS = (
    (
        "module",
        "export NODE_PATH=/app/node_modules && npx browserify {infile} -t \
            [ babelify --presets [ @babel/preset-env ] ] > {outfile}",
    ),
    (
        "text/jsx",
        "export NODE_PATH=/app/node_modules && npx browserify {infile} -t \
            [ babelify --presets [ @babel/preset-env @babel/preset-react ] ] > {outfile}",
    ),
)

COMPRESS_OUTPUT_DIR = 'compressor'

COMPRESS_ENABLED = True

# Enable offline compression in production only
COMPRESS_OFFLINE = not DEBUG

# Make sure Django compressor can generate static paths
COMPRESS_OFFLINE_CONTEXT = {'static': static}
