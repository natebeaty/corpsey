from django.utils import simplejson
from corpsey.apps.comics.models import Comic
from dajaxice.decorators import dajaxice_register
from easy_thumbnails.files import get_thumbnailer

@dajaxice_register
def get_comic_panels(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    comic_links = comic.get_comic_links()
    comic_links_arr = []
    if comic_links:
        for link in comic_links:
            comic_links_arr.append({ 'comic_id': link.id, 'last_name': link.artist.last_name, 'comic_1': comic_id })
    prev_sib = ''
    if comic.prev_sib():
        prev_sib = comic.prev_sib().id
    return simplejson.dumps({ 
        'panel1' : get_thumbnailer(comic.panel1)['midsize'].url, 
        'panel2' : get_thumbnailer(comic.panel2)['midsize'].url, 
        'panel3' : get_thumbnailer(comic.panel3)['midsize'].url,
        'comic_id' : comic_id,
        'comic_links' : comic_links_arr,
        'prev_sib' : prev_sib,
        'last_name' : comic.artist.last_name,
    })
