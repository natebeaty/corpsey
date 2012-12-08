from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext

def home(request):
    page = get_object_or_404(FlatPage,url='/catacombs/')
    return render_to_response('comics/home.html',  {
        'page': page,
        'comics': Comic.objects.all(),
        }, RequestContext(request))

def random(request):
    comic_to = Comic.objects.order_by('?')[0]
    return redirect(comic_to)

def entry(request, comic_1, comic_2=None):
    comic_links = []
    comic_1 = get_object_or_404(Comic,pk=comic_1)
    
    if comic_2:
        comic_2 = get_object_or_404(Comic,pk=comic_2)
        next_sib = comic_2.get_next_sibling()
        if next_sib:
            comic_links.append(next_sib)
        children = comic_2.get_children()
        if children:
            comic_links.append(children[0])
    else:
        # build next/child comic nav if possible
        next_sib = comic_1.get_next_sibling()
        if next_sib:
            comic_links.append(next_sib)
        children = comic_1.get_children()
        if children:
            comic_links.append(children[0])
        comic_2 = None

    return render_to_response('comics/entry.html',  {
        'comic_1': comic_1,
        'comic_2': comic_2,
        'comic_links': comic_links,
        'active_comics': [comic_1, comic_2],
        'comics': Comic.objects.all(),
        }, RequestContext(request))


    
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from corpsey.apps.comics.forms import UploadForm

def contribute(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            comic = Comic(
                panel1 = request.FILES['panel1'],
                panel2 = request.FILES['panel2'],
                panel3 = request.FILES['panel3']
            )
            comic.save()
            # return HttpResponseRedirect(reverse('myapp.views.list'))
    else:
        form = UploadForm()


    # Render list page with the documents and the form
    return render_to_response(
        'corpsey/comics/contribute.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
