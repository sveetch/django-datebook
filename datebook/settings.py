"""
Default Datebook settings to import/define in your project settings
"""

# Add new specific "rstview" parser settings for Forum app, if you have other apps 
# that define parser settings this can lead to overwrite problems. In this 
# case, just define all parser setting in 'RSTVIEW_PARSER_FILTER_SETTINGS' in 
# the same settings file.
RSTVIEW_PARSER_FILTER_SETTINGS = {
    'datebook':{
        'initial_header_level': 5,
        'file_insertion_enabled': False,
        'raw_enabled': False,
        'footnote_references': 'superscript',
        'doctitle_xform': False,
    },
}

#
# Optionnal text markup settings
#

# Field helper for texts in forms
DATEBOOK_TEXT_FIELD_HELPER_PATH = None # Default, just a CharField
#DATEBOOK_TEXT_FIELD_HELPER_PATH = "datebook.markup.get_text_field" # Use DjangoCodeMirror

# Validator helper for texts in forms
DATEBOOK_TEXT_VALIDATOR_HELPER_PATH = None # Default, no markup validation
#DATEBOOK_TEXT_VALIDATOR_HELPER_PATH = "datebook.markup.clean_restructuredtext" # Validation for RST syntax (with Rstview)

# Text markup renderer
DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE = None # Default, just a CharField
#DATEBOOK_TEXT_MARKUP_RENDER_TEMPLATE = "datebook/markup/_text_markup_render.html" # Use Rstview renderer

# Template to init some Javascript for texts in forms
DATEBOOK_TEXT_FIELD_JS_TEMPLATE = None # Default, no JS template
#DATEBOOK_TEXT_FIELD_JS_TEMPLATE = "datebook/markup/_text_field_djangocodemirror_js.html" # Use DjangoCodeMirror
