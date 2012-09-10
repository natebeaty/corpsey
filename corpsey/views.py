from apps.comics.models import *
# from apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def home(request):
    comic_set = Comic.objects.filter(active=True).order_by('-date')[:5]
    return render_to_response('home.html',  {
        'title': '',
        'comic_set': comic_set,
        }, RequestContext(request))
