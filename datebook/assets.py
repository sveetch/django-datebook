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
    }

    ENABLED_BUNDLES = (
        'datebook_frontend_css',
    )

    for item in ENABLED_BUNDLES:
        register(item, AVALAIBLE_BUNDLES[item])
