from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext

def home(request):
    page = get_object_or_404(FlatPage,url='/catacombs/')
    return render_to_response('comics/home.html',  {
        'page': page,
        'comics': Comic.objects.all(),
        }, RequestContext(request))

def random(request):
    comic_to = Comic.objects.order_by('?')[0]
    return redirect(comic_to)

def entry(request, comic_1, comic_2=None):
    comic_1 = get_object_or_404(Comic,pk=comic_1)
    if comic_2:
        comic_2 = get_object_or_404(Comic,pk=comic_2)
    else:
        comic_2 = None
    return render_to_response('comics/entry.html',  {
        'comic_1': comic_1,
        'comic_2': comic_2,
        'active_comics': [comic_1, comic_2],
        'comics': Comic.objects.all(),
        }, RequestContext(request))
    