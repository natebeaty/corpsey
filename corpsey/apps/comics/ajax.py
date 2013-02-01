from django.utils import simplejson
from corpsey.apps.comics.models import Comic
from dajaxice.decorators import dajaxice_register
from easy_thumbnails.files import get_thumbnailer

@dajaxice_register(method='GET')
def get_comic_panels(request, comic_id, direction):
    comic = Comic.objects.get(pk=comic_id)

    return simplejson.dumps({ 
        'panel1' : get_thumbnailer(comic.panel1)['midsize'].url, 
        'panel2' : get_thumbnailer(comic.panel2)['midsize'].url, 
        'panel3' : get_thumbnailer(comic.panel3)['midsize'].url,
        'comic_id' : comic_id,
        'direction' : direction,
        'first_name' : comic.artist.first_name,
        'last_name' : comic.artist.last_name,
    })

@dajaxice_register(method='GET')
def get_nav_links(request, comic_id, comic_id_2):
    up_comic_links = 0;
    comic_2 = Comic.objects.get(pk=comic_id_2)
    next_comic_links = comic_2.get_next_comic_links()
    next_comic_links_arr = []
    if next_comic_links:
        for link in next_comic_links:
            next_comic_links_arr.append({ 
                'comic_id': link.id, 
                'first_name': link.artist.first_name, 
                'last_name': link.artist.last_name, 
            })
    else:
        if comic_2.is_child_node:
            up_comic_links = 1;

    comic = Comic.objects.get(pk=comic_id)
    prev_comic_links = comic.get_prev_comic_links()
    prev_comic_links_arr = []
    if prev_comic_links:
        for link in prev_comic_links:
            prev_comic_links_arr.append({ 
                'comic_id': link.id, 
                'first_name': link.artist.first_name, 
                'last_name': link.artist.last_name, 
            })

    return simplejson.dumps({ 
        'prev_comic_links' : prev_comic_links_arr,
        'next_comic_links' : next_comic_links_arr,
        'up_comic_links' : up_comic_links,
    })
