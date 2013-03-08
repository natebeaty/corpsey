from apps.comics.models import *
# from apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from datetime import datetime, timedelta

def home(request):
    comic_set = Comic.objects.filter(active=True, date__gte=datetime.now()-timedelta(days=7)).order_by('-date')
    # if less than 10 in last week, just pull last 10!
    if len(comic_set) < 10:
	    comic_set = Comic.objects.filter(active=True).order_by('-date')[:10]
    page = FlatPage.objects.get(url='/')
    num_artists = Artist.objects.count()
    return render_to_response('home.html',  {
        'title': '',
        'page': page,
        'num_artists': num_artists,
        'comic_set': comic_set,
        }, RequestContext(request))
