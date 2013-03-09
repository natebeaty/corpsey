from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.core.mail import mail_admins,mail_managers
from django.core import urlresolvers
from easy_thumbnails.files import get_thumbnailer
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

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
        # todo: add uturn to end of children
    return result

def tree(request):
    page = get_object_or_404(FlatPage,url='/tree/')

    return render_to_response('comics/tree.html',  {
        'page': page,
        'comics': Comic.objects.filter(active=True),
        }, RequestContext(request))

@cache_page(60 * 15)
def tree_json(request):
    import json
    from mptt.templatetags.mptt_tags import cache_tree_children

    root_nodes = cache_tree_children(Comic.objects.filter(active=True))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
    root = {
        'name': 'corpsey',
        'children': dicts,
    }
    return HttpResponse(json.dumps(root, indent=4), mimetype="application/json")

def random(request):
    from django.db.models import F
    comic_leaf = Comic.objects.filter(level__gt=0).order_by('?')[0]
    return redirect('/catacombs/%d/%d/' % (comic_leaf.parent.id, comic_leaf.id,))

def random_starter(request):
    comic_to = Comic.objects.filter(starter=True).order_by('?')[0]
    return redirect(comic_to)

def artist_in_catacombs(request, artist):
    artist = get_object_or_404(Artist,pk=artist)
    comic_to = Comic.objects.filter(artist_id=artist.id).order_by('?')[0]
    if not comic_to.is_root_node():
        url = '/catacombs/%d/%d/' % (comic_to.parent.id, comic_to.id)
    else:
        url = comic_to.get_absolute_url()
    return redirect(url)

@cache_page(60 * 15)
def entry(request, comic_1, comic_2=None):
    next_comic_links = []
    uturn = []
    comic_1 = get_object_or_404(Comic,pk=comic_1)
    
    # build next/child comic nav if possible
    if comic_2:
        comic_2 = get_object_or_404(Comic,pk=comic_2)
        next_comic_links.extend(comic_2.get_next_comic_links())
    else:
        next_comic_links.extend(comic_1.get_next_comic_links())

    prev_comic_links = comic_1.get_prev_comic_links()

    if not next_comic_links and comic_2:
        uturn = comic_2.get_uturn()

    return render_to_response('comics/entry.html',  {
        'comic_1': comic_1,
        'comic_2': comic_2,
        'uturn': uturn,
        'next_comic_links': next_comic_links,
        'prev_comic_links': prev_comic_links,
        }, RequestContext(request))

@cache_page(60 * 15)
def uturn(request, uturn, comic=None):
    uturn = get_object_or_404(Uturn,pk=uturn)
    prev_comic_links = []
    next_comic_links = []
    
    if comic:
        comic = get_object_or_404(Comic,pk=comic)
        prev_comic_links.extend(comic.get_prev_comic_links())
        next_comic_links = [uturn.portal_to]
    else:
        next_comic_links.extend(uturn.portal_to.get_next_comic_links())


    return render_to_response('comics/uturn_entry.html',  {
        'uturn': uturn,
        'comic': comic,
        'next_comic_links': next_comic_links,
        'prev_comic_links': prev_comic_links,
        }, RequestContext(request))

def contributions(request):
    contributions = Contribution.objects.filter(pending=True)

    return render_to_response('comics/contributions.html',  {
        'contribution_set': contributions
        }, RequestContext(request))

def contribute(request):
    from django.db.models import F
    from corpsey.apps.comics.forms import ContributeForm

    parent_comic = Comic.objects.filter(lft=F('rght')-1).order_by('?')[0]
    step = 1
    message = ''
    # form sent!
    if request.method == 'POST':
        form = ContributeForm(request.POST)
        if form.is_valid():
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import get_template
            from django.template import Context
            from django.conf import settings
            import base64, md5, hashlib, time, os

            comic_id = form.cleaned_data['comic_id']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            parent_comic = Comic.objects.get(pk=comic_id)
            code = base64.urlsafe_b64encode(hashlib.md5(str(time.time())).digest())[:15]

            # check if email has pending contributions
            try:
                existing_contribution = Contribution.objects.get(email=email,pending=True)
                message = 'The email %s already has a pending contribution. Please check your email for instructions on uploading your panels.' % email
            except:
                # store contribution in db
                contribution = Contribution(
                    code = code,
                    email = email,
                    name = name,
                    comic = parent_comic,
                )
                contribution.save()

                plaintext = get_template('emails/contribute_invite_email.txt')
                htmly     = get_template('emails/contribute_invite_email.html')

                d = Context({ 
                    'comic': parent_comic,
                    'parent_comic_url': parent_comic.get_absolute_url(),
                    'code': code,
                    })

                subject, from_email, to = 'Infinite Corpsey Confirmation', 'corpsey@trubbleclub.com', email
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    message = 'Email sent ok!'
                except:
                    message = 'There was an error sending your confirmation email. Please write nate@trubbleclub.com for help.'
                step = 2
        else:
            message = "oh no!"
    else:
        form = ContributeForm({ 'comic_id': parent_comic.id })

    page = FlatPage.objects.get(url='/contribute/')
    page2 = FlatPage.objects.get(url='/contribute/ok/')

    return render_to_response(
        'comics/contribute.html',
        {
            'message': message,
            'step': step,
            'page': page,
            'page2': page2,
            'parent_comic': parent_comic,
            'contribute_form': form
        },
        context_instance=RequestContext(request))


def contribute_upload(request, upload_code):
    from django.http import HttpResponseRedirect
    from django.core.urlresolvers import reverse
    from corpsey.apps.comics.forms import UploadForm

    from django.db.models import F
    message = ''
    step = 1
    page = FlatPage.objects.get(url='/contribute/upload/')
    page2 = FlatPage.objects.get(url='/contribute/upload/ok/')
    try:
        contribution = Contribution.objects.get(code=upload_code)
        parent_comic = contribution.comic
        form = UploadForm({'name': contribution.name, 'email': contribution.email})

        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                contribution.panel1 = request.FILES['panel1']
                contribution.panel2 = request.FILES['panel2']
                contribution.panel3 = request.FILES['panel3']
                contribution.save()

                message = "Contribution uploaded ok!"
                step = 2

                # Email managers
                # admin_link = urlresolvers.reverse('admin:comics_contribution_change', args=(contribution.id,))
                # mail_subject = 'New Corpsey Submission!'
                # mail_body = 'Title: %s\n\nEdit: http://%s%s\n' % (contribution, request.META['HTTP_HOST'], admin_link)
                # mail_admins(mail_subject, mail_body, fail_silently=False)

                # return HttpResponseRedirect(reverse('myapp.views.contribute'))

            else:
                message = "oh no!"
    except Contribution.DoesNotExist:
        message = 'Contribution code <i>%s</i> was not found!' % upload_code
        return render_to_response(
            'comics/contribute_upload.html', 
            { 'message': message },
            context_instance=RequestContext(request)
        )

    return render_to_response(
        'comics/contribute_upload.html',
        {
            'upload_code': upload_code,
            'step': step,
            'form': form,
            'page': page,
            'page2': page2,
            'parent_comic': parent_comic,
            'message': message
        },
        context_instance=RequestContext(request)
    )



                # look for artist or add new
                # try:
                #     artist = Artist.objects.get(name=form.cleaned_data['name'])
                # except:
                #     artist = Artist(name=form.cleaned_data['name'])
                # artist.email=form.cleaned_data['email']
                # if form.cleaned_data['website']:
                #     artist.website=form.cleaned_data['website']
                # artist.save()

                # comic = Comic(
                #     artist = artist,
                #     panel1 = request.FILES['panel1'],
                #     panel2 = request.FILES['panel2'],
                #     panel3 = request.FILES['panel3']
                # )
                # comic.save()
