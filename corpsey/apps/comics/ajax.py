from django.utils import simplejson
from corpsey.apps.comics.models import Comic
from dajaxice.decorators import dajaxice_register
from easy_thumbnails.files import get_thumbnailer

@dajaxice_register(method='GET')
def get_comic_panels(request, comic_id, direction, hdpi_enabled):
    comic = Comic.objects.get(pk=comic_id)
    size = 'midsize_hd' if hdpi_enabled else 'midsize'
    if comic:
        comic_obj = {
            'panel1' : get_thumbnailer(comic.panel1)[size].url, 
            'panel2' : get_thumbnailer(comic.panel2)[size].url, 
            'panel3' : get_thumbnailer(comic.panel3)[size].url,
            'comic_id' : comic.id,
            'first_name' : comic.artist.first_name,
            'last_name' : comic.artist.last_name,
            'name' : comic.artist.name
        }
    else:
        comic_obj = {}

    return simplejson.dumps({ 
        'direction' : direction,
        'comic' : comic_obj
    })

@dajaxice_register(method='GET')
def get_nav_links(request, comic_id_arr):
    up_comic_links = 0;

    comic = Comic.objects.get(pk=comic_id_arr[0])
    prev_comic_links = comic.get_prev_comic_links()
    prev_comic_links_arr = []
    if prev_comic_links:
        for link in prev_comic_links:
            prev_comic_links_arr.append({ 
                'comic_id': link.id, 
                'comic_id_2': comic.id,
                'first_name': link.artist.first_name, 
                'last_name': link.artist.last_name, 
                'name': link.artist.name, 
            })

    if len(comic_id_arr) == 1:
        comic = Comic.objects.get(pk=comic_id_arr[0])
    else:
        comic = Comic.objects.get(pk=comic_id_arr[1])

    next_comic_links = comic.get_next_comic_links()
    next_comic_links_arr = []
    if next_comic_links:
        for link in next_comic_links:
            next_comic_links_arr.append({ 
                'comic_id': link.id, 
                'comic_id_2': comic.id,
                'first_name': link.artist.first_name, 
                'last_name': link.artist.last_name, 
                'name': link.artist.name, 
            })
    else:
        if comic.is_child_node:
            up_comic_links = 1;

    return simplejson.dumps({ 
        'prev_comic_links' : prev_comic_links_arr,
        'next_comic_links' : next_comic_links_arr,
        'up_comic_links' : up_comic_links,
    })
