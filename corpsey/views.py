from apps.comics.models import *
# from apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def home(request):
    comic_set = Comic.objects.filter(active=True).order_by('-date')[:10]
    page = FlatPage.objects.get(url='/')
    num_artists = Artist.objects.filter(comics!=None).count()
    return render_to_response('home.html',  {
        'title': '',
        'page': page,
        'num_artists': num_artists,
        'comic_set': comic_set,
        }, RequestContext(request))

@cache_page(60 * 15)
def artists(request):
    artist_set = Artist.objects.filter(comics!=None).order_by('name')
    page = FlatPage.objects.get(url='/artists/')
    return render_to_response('artists.html',  {
        'title': page.title,
        'page': page,
        'artist_set': artist_set,
        }, RequestContext(request))

@cache_page(60 * 15)
def about(request):
    page = FlatPage.objects.get(url='/about/')
    return render_to_response('about.html',  {
        'title': page.title,
        'page': page,
        }, RequestContext(request))

