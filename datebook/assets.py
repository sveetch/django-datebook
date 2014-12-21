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
        'datebook_app_css': Bundle(
            "css/datebook_app.css",
            filters='yui_css',
            output='css/datebook_app.min.css'
        ),
        'datebook_app_js': Bundle(
            "js/jquery/jquery.timepicker.js",
            "js/jquery/moment.js",
            "js/jquery/pikaday.js",
            "js/datebook/day_form.js",
            "js/datebook/calendar.js",
            filters='yui_js',
            output='js/datebook_app.min.js'
        ),
    }

    ENABLED_BUNDLES = (
        'datebook_app_css',
        'datebook_app_js',
    )

    for item in ENABLED_BUNDLES:
        register(item, AVALAIBLE_BUNDLES[item])
