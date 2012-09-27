from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext

def home(request):
    page = get_object_or_404(FlatPage,url='/catacomb/')
    return render_to_response('comics/home.html',  {
        'page': page,
        }, RequestContext(request))
