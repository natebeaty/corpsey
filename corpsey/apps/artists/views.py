from corpsey.apps.artists.models import *
from corpsey.apps.comics.models import *
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render

def entry(request, artist_id):
    pass

@cache_page(60 * 15)
def artists(request):
    q = request.GET.get('term', '')
    if q:
        artist_set = Artist.objects.exclude(comics=None).filter(name__icontains = q )
    else:
        artist_set = Artist.objects.exclude(comics=None).order_by('last_name')
    page = FlatPage.objects.get(url='/artists/')
    return render(request, 'artists.html',  {
        'title': page.title,
        'page': page,
        'q': q,
        'artist_set': artist_set,
        })

def get_artists(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        artists = Artist.objects.exclude(comics=None).filter(name__icontains = q )[:20]
        results = []
        for artist in artists:
            url = ''
            comics = Comic.objects.filter(artist_id = artist.id)
            if len(comics) > 0:
                url = comics[0].get_absolute_url()
            artist_json = {}
            artist_json['id'] = artist.id
            artist_json['label'] = artist.name
            artist_json['url'] = url
            artist_json['value'] = artist.name
            results.append(artist_json)

            # artist_json['comics'] = []
            # if artist.num_comics > 1:
            #   for comic in artist.comics.all()[1:]:
            #     artist_json['comic_urls']
            #   endfor
            # endif

        data = results
    else:
        data = 'fail'
    return JsonResponse(data, safe=False)