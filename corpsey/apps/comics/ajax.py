from django.utils import simplejson
from corpsey.apps.comics.models import *
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
            'name' : comic.artist.name,
            'url' : comic.artist.url,
        }
    else:
        comic_obj = {}

    return simplejson.dumps({ 
        'direction' : direction,
        'comic' : comic_obj
    })

@dajaxice_register(method='GET')
def contribution_vote(request, contribution_id, yea, rule_broke):
    contribution = Contribution.objects.get(pk=contribution_id)
    approve = True if yea == 1 else False

    if rule_broke == 0:
        rule_broke = None
    else:
        rule_broke = Rule.objects.get(pk=rule_broke)

    vote = Vote(
        contribution = contribution,
        user = request.user,
        approve = approve,
        rule_broke = rule_broke,
        )
    vote.save()
    return simplejson.dumps({ 
        'contribution_id' : contribution_id,
        'yea' : yea
    })

@dajaxice_register(method='GET')
def get_new_leaf(request, comic_id, hdpi_enabled):
    from django.db.models import F
    size = 'midsize_hd' if hdpi_enabled else 'midsize'
    comic = Comic.objects.filter(lft = F('rght')-1).exclude(id = comic_id).order_by('?')[0]
    comic_obj = {
        'panel1' : get_thumbnailer(comic.panel1)[size].url, 
        'panel2' : get_thumbnailer(comic.panel2)[size].url, 
        'panel3' : get_thumbnailer(comic.panel3)[size].url,
        'comic_id' : comic.id,
        'first_name' : comic.artist.first_name,
        'last_name' : comic.artist.last_name,
        'name' : comic.artist.name,
        'url' : comic.artist.url,
    }
    return simplejson.dumps({ 
        'comic' : comic_obj
    })

@dajaxice_register(method='GET')
def get_nav_links(request, comic_id_arr):
    up_comic_links = {};

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
            if (comic.get_uturn()):
                up_comic_links = {
                    'comic_id': comic.id,
                    'id': comic.get_uturn()[0].id,
                    'uturn_comic_id': comic.get_uturn()[0].portal_to.id,
                    'uturn_name': 'Trubble Club'
                };

    return simplejson.dumps({ 
        'prev_comic_links' : prev_comic_links_arr,
        'next_comic_links' : next_comic_links_arr,
        'up_comic_links' : up_comic_links,
    })
