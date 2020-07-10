# Taken from http://stackoverflow.com/a/1433970/1178426
from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    Returns analytics code.
    """
    if settings.GOOGLE_ANALYTICS_KEY:
        return { 'analytics_code': render_to_string("analytics.html", { 'google_analytics_key': settings.GOOGLE_ANALYTICS_KEY }) }
    else:
        return { 'analytics_code': "" }
