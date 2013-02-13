from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.core.mail import mail_admins,mail_managers
from django.core import urlresolvers
from easy_thumbnails.files import get_thumbnailer
from django.http import HttpResponse

def home(request):
    page = get_object_or_404(FlatPage,url='/catacombs/')
    return render_to_response('comics/home.html',  {
        'page': page,
        'comics': Comic.objects.all().filter(active=True),
        }, RequestContext(request))


import json
from mptt.templatetags.mptt_tags import cache_tree_children

def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'size': node.pk*100,
        'url': node.get_absolute_url(),
        'image': get_thumbnailer(node.panel1)['midsize'].url,
        'name': node.artist.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result

def tree(request):
    page = get_object_or_404(FlatPage,url='/tree/')

    return render_to_response('comics/tree.html',  {
        'page': page,
        'comics': Comic.objects.all().filter(active=True),
        }, RequestContext(request))

def tree_json(request):
    root_nodes = cache_tree_children(Comic.objects.all().filter(active=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
    root = {
        'name': 'corpsey',
        'children': dicts,
    }
    return HttpResponse(json.dumps(root, indent=4), mimetype="application/json")

def random(request):
    comic_to = Comic.objects.order_by('?')[0]
    return redirect(comic_to)

def random_starter(request):
    comic_to = Comic.objects.all().filter(starter=True).order_by('?')[0]
    return redirect(comic_to)

def entry(request, comic_1, comic_2=None):
    next_comic_links = []
    comic_1 = get_object_or_404(Comic,pk=comic_1)
    
    # build next/child comic nav if possible
    if comic_2:
        comic_2 = get_object_or_404(Comic,pk=comic_2)
        next_comic_links.extend(comic_2.get_next_comic_links())
    else:
        next_comic_links.extend(comic_1.get_next_comic_links())

    prev_comic_links = comic_1.get_prev_comic_links()

    return render_to_response('comics/entry.html',  {
        'comic_1': comic_1,
        'comic_2': comic_2,
        'next_comic_links': next_comic_links,
        'prev_comic_links': prev_comic_links,
        'active_comics': [comic_1, comic_2],
        'comics': Comic.objects.all().filter(active=True),
        }, RequestContext(request))


    
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from corpsey.apps.comics.forms import UploadForm

def contribute(request):
    message = ''
    page = FlatPage.objects.get(url='/contribute/')
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # parent sent?
            # if form.parent_id:
            #     parent = Comic(pk=form.cleaned_data.parent_id)
            # else:
            #     parent = null

            # look for artist or add new
            try:
                artist = Artist.objects.get(name=form.cleaned_data['name'])
            except:
                artist = Artist(name=form.cleaned_data['name'])
            artist.email=form.cleaned_data['email']
            if form.cleaned_data['website']:
                artist.website=form.cleaned_data['website']
            artist.save()

            comic = Comic(
                artist = artist,
                panel1 = request.FILES['panel1'],
                # panel2 = request.FILES['panel2'],
                # panel3 = request.FILES['panel3']
            )
            comic.save()
            message = "Comic saved ok! %s" % comic.get_absolute_url()

            # Email managers
            admin_link = urlresolvers.reverse('admin:comics_comic_change', args=(comic.id,))
            mail_subject = 'New Corpsey Submission!'
            mail_body = 'Title: %s\n\nEdit: http://%s%s\n' % (comic, request.META['HTTP_HOST'], admin_link)
            mail_admins(mail_subject, mail_body, fail_silently=False)

            # return HttpResponseRedirect(reverse('myapp.views.contribute'))

        else:
            message = "oh no!"
    else:
        form = UploadForm()


    # Render list page with the documents and the form
    return render_to_response(
        'comics/contribute.html',
        {
            'form': form,
            'page': page,
            'message': message
        },
        context_instance=RequestContext(request)
    )

