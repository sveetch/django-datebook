"""
Asset bundles to use with django-assets
"""
try:
    from django_assets import Bundle, register
except ImportError:
    DJANGO_ASSETS_INSTALLED = False
else:
    DJANGO_ASSETS_INSTALLED = True

    AVALAIBLE_BUNDLES = {
        'datebook_frontend_css': Bundle(
            "css/datebook/frontend.css",
            filters='yui_css',
            output='css/datebook/frontend.min.css'
        ),
        'datebook_frontend_js': Bundle(
            "js/jquery/jquery.timepicker.js",
            "js/jquery/moment.js",
            filters='yui_js',
            output='js/datebook_frontend.min.js'
        ),
    }

    ENABLED_BUNDLES = (
        'datebook_frontend_css',
        'datebook_frontend_js',
    )

    for item in ENABLED_BUNDLES:
        register(item, AVALAIBLE_BUNDLES[item])
