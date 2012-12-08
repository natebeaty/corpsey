from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext

def home(request):
    page = get_object_or_404(FlatPage,url='/catacombs/')
    return render_to_response('comics/home.html',  {
	    'page': page,
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
