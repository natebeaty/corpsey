from corpsey.apps.artists.models import *
from corpsey.apps.comics.models import *
from django.http import HttpResponse
import json

def entry(request, artist_id):
    pass

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
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)