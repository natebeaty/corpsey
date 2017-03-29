from apps.comics.models import *
from apps.artists.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.views.decorators.cache import cache_page

@login_required()
def logout_view(request):
    """Custom logout with redirect."""
    logout(request)
    return redirect('/?logged_out_ok=1')

@cache_page(60 * 15)
def home(request):
    comic_set = Comic.objects.filter(active=True).order_by('-date')[:10]
    page = FlatPage.objects.get(url='/')
    num_artists = Artist.objects.exclude(comics=None).count()
    return render(request, 'home.html',  {
        'title': '',
        'page': page,
        'num_artists': num_artists,
        'comic_set': comic_set,
        })

@cache_page(60 * 15)
def artists(request):
    artist_set = Artist.objects.exclude(comics=None).order_by('last_name')
    page = FlatPage.objects.get(url='/artists/')
    return render(request, 'artists.html',  {
        'title': page.title,
        'page': page,
        'artist_set': artist_set,
        })

@cache_page(60 * 15)
def about(request):
    page = FlatPage.objects.get(url='/about/')
    return render(request, 'about.html',  {
        'title': page.title,
        'page': page,
        })

