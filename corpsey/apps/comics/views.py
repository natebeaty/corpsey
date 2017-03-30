from corpsey.apps.comics.models import *
from corpsey.apps.artists.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext
from django.core.mail import send_mass_mail
from django.core import urlresolvers
from easy_thumbnails.files import get_thumbnailer
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'size': node.pk*100,
        'url': node.get_absolute_url(),
        # 'image': get_thumbnailer(node.panel1)['midsize'].url,
        'name': node.artist.name,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
        # TODO: add uturn to end of children
    return result

@cache_page(60 * 15)
def tree(request):
    """Fancy tree browsing."""
    page = get_object_or_404(FlatPage,url='/tree/')

    return render(request, 'comics/tree.html',  {
        'page': page,
        'comics': Comic.objects.filter(active=True),
    })

@cache_page(60 * 15)
def tree_json(request):
    """Json view for the tree page."""
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
    return HttpResponse(json.dumps(root, indent=4), mimetype='application/json')

@cache_page(60 * 15)
def featured(request):
    comic_set = Comic.objects.filter(active=True,featured=True).order_by('-date')[:10]
    return render(request, 'featured.html',  {
        'comic_set': comic_set,
    })

def random(request):
    """Return a random comic that's not a root."""
    comic_leaf = Comic.objects.filter(level__gt=0).order_by('?')[0]
    request.session['last_comic_id'] = comic_leaf.id
    return redirect('/catacombs/%d/%d/' % (comic_leaf.parent.id, comic_leaf.id,))

def enter_the_catacombs(request):
    """Return a random comic marked as a starter for Enter the Catacombs button on homepage."""
    comic_to = Comic.objects.filter(starter=True).order_by('?')[0]
    return redirect(comic_to)

def artist_in_catacombs(request, artist, num):
    """Redirect to a comic for an artist."""
    artist = get_object_or_404(Artist,pk=artist)
    try:
        comic_to = artist.comics.all()[int(num) - 1]
        url = comic_to.get_absolute_url()
    except:
        url = '/artists/'
    return redirect(url)

@cache_page(60 * 15)
def entry(request, comic_1, comic_2=None):
    """Page in the catacombs, one or two comics."""
    next_comic_links = []
    uturn = []

    # Store comic_id for /contribute/
    request.session['last_comic_id'] = comic_1

    comic_1 = get_object_or_404(Comic,pk=comic_1)

    # Build next/child comic nav if possible
    if comic_2:
        request.session['last_comic_id'] = comic_2
        comic_2 = get_object_or_404(Comic,pk=comic_2)
        next_comic_links.extend(comic_2.get_next_comic_links())
    else:
        next_comic_links.extend(comic_1.get_next_comic_links())

    prev_comic_links = comic_1.get_prev_comic_links()

    if not next_comic_links and comic_2:
        uturn = comic_2.get_uturn()

    return render(request, 'comics/entry.html',  {
        'comic_1': comic_1,
        'comic_2': comic_2,
        'uturn': uturn,
        'next_comic_links': next_comic_links,
        'prev_comic_links': prev_comic_links,
    })

def pad_panels(request, contribution):
    """Add 40px of white padding to comic panels."""
    import subprocess
    contribution = get_object_or_404(Contribution,pk=contribution)

    command = "convert -bordercolor White -border 20 %s%s %s%s " % (settings.MEDIA_ROOT, contribution.panel1, settings.MEDIA_ROOT, contribution.panel1)
    command += "&& convert -bordercolor White -border 20 %s%s %s%s " % (settings.MEDIA_ROOT, contribution.panel2, settings.MEDIA_ROOT, contribution.panel2)
    command += "&& convert -bordercolor White -border 20 %s%s %s%s " % (settings.MEDIA_ROOT, contribution.panel3, settings.MEDIA_ROOT, contribution.panel3)
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    stdout_value = proc.communicate()[0]

    return HttpResponse('20px of white padding added to contribution panels ok!')

@cache_page(60 * 15)
def uturn(request, uturn, comic=None):
    """Motherfucking uturns."""
    uturn = get_object_or_404(Uturn,pk=uturn)
    prev_comic_links = []
    next_comic_links = []

    if comic:
        comic = get_object_or_404(Comic,pk=comic)
        prev_comic_links.extend(comic.get_prev_comic_links())
        next_comic_links = [uturn.portal_to]
    else:
        next_comic_links.extend(uturn.portal_to.get_next_comic_links())


    return render(request, 'comics/uturn_entry.html',  {
        'uturn': uturn,
        'comic': comic,
        'next_comic_links': next_comic_links,
        'prev_comic_links': prev_comic_links,
    })

@login_required()
def contributions(request):
    """Page for the elders to vote YAY or NAY on contributions."""
    user_votes = Vote.objects.filter(user_id=request.user.id)
    # Omit contributions user has already voted on AND contributions that have no panels yet (todo: has_uploaded boolean field?)
    contributions = Contribution.objects.filter(pending=True, has_panels=True).exclude(id__in=user_votes.values_list('contribution_id', flat=True))
    rules = Rule.objects.all().order_by('-id')

    return render(request, 'comics/contributions.html',  {
        'user_votes': user_votes,
        'rules': rules,
        'contributions': contributions,
    })

@login_required()
def graveyard(request):
    """Mass graveyard of rejected contributions."""
    user_votes = Vote.objects.filter(user_id=request.user.id)
    graves_list = Contribution.objects.filter(pending=False, has_panels=True, accepted=False).order_by('-date')
    paginator = Paginator(graves_list, 10)
    page = request.GET.get('page')

    try:
        graves = paginator.page(page)
    except PageNotAnInteger:
        graves = paginator.page(1)
    except EmptyPage:
        graves = paginator.page(paginator.num_pages)

    return render(request, 'comics/graveyard.html',  {
        'graves': graves,
    })

def contribute(request):
    """Reserve a spot to contribute after a comic."""
    from corpsey.apps.comics.forms import ContributeForm

    step = 1
    message = ''

    # ?parent=x
    if request.GET.get('parent', False):
        try:
            parent_id = int(request.GET['parent'])
            try:
                parent_comic = Comic.objects.get(pk=parent_id)
                if not parent_comic.valid_to_follow():
                    message = 'Sorry, comic #%s is not valid to follow, random one chosen.' % request.GET['parent']
                    parent_comic = find_comic_to_follow()
            except Comic.DoesNotExist:
                message = 'Unable to locate comic #%s for parent, random one chosen.' % request.GET['parent']
                parent_comic = find_comic_to_follow()
        except ValueError:
            message = '"%s" doesn\'t seem to be a number.' % request.GET['parent']
            parent_comic = find_comic_to_follow()
    elif request.session.get('last_comic_id', False):
        parent_comic = Comic.objects.get(pk=request.session['last_comic_id'])
        # Only use last_comic_id once
        request.session['last_comic_id'] = None
        if not parent_comic.valid_to_follow():
            parent_comic = find_comic_to_follow()
    else:
        parent_comic = find_comic_to_follow()

    # Form sent!
    if request.method == 'POST':
        form = ContributeForm(request.POST)
        if form.is_valid():
            from django.core.mail import EmailMultiAlternatives
            from django.template.loader import get_template
            from django.template import Context
            import base64, md5, hashlib, time, os

            comic_id = form.cleaned_data['comic_id']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            try:
                parent_comic = Comic.objects.get(pk=comic_id)
            except Comic.DoesNotExist:
                return HttpResponse('Unable to locate comic #%s for parent. You broke HAL!' % comic_id)

            code = base64.urlsafe_b64encode(hashlib.md5(str(time.time())).digest())[:15]

            # Check if email has pending contributions
            try:
                existing_contribution = Contribution.objects.get(email=email,pending=True)
                message = 'The email %s already has a pending contribution. Please check your email for instructions on uploading your panels.' % email
            except:
                # Store contribution in db
                contribution = Contribution(
                    code = code,
                    email = email,
                    name = name,
                    deadline = timezone.now()+timedelta(days=7),
                    comic = parent_comic,
                )
                contribution.save()

                plaintext = get_template('emails/contribution_invite.txt')
                htmly     = get_template('emails/contribution_invite.html')

                d = Context({
                    'comic': parent_comic,
                    'parent_comic_url': parent_comic.get_absolute_url(),
                    'code': code,
                    })

                subject = 'Infinite Corpse Confirmation'
                from_email = 'corpsey@trubble.club'
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                try:
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    message = 'Email sent to %s ok!' % email
                except:
                    message = 'There was an error sending your confirmation email. Please write nate@trubble.club for help.'
                step = 2
        else:
            message = "Oh no! Corpsey robot brain broke with your data."
    else:
        form = ContributeForm(initial={ 'comic_id': parent_comic.id })

    page = FlatPage.objects.get(url='/contribute/')
    page2 = FlatPage.objects.get(url='/contribute/ok/')
    deadline = timezone.now()+timedelta(days=7)

    return render(request, 'comics/contribute.html', {
        'message': message,
        'deadline': deadline,
        'step': step,
        'page': page,
        'page2': page2,
        'parent_comic': parent_comic,
        'contribute_form': form
    })

def find_comic_to_follow(exclude=0):
    """Loop through comic leafs to find one with less than MAX_COMIC_CHILDREN children + pending contributions."""
    comic_leafs = Comic.objects.filter(level__gt=0).exclude(id = exclude).order_by('?')
    for comic in comic_leafs:
        if comic.valid_to_follow():
            return comic
    return None

def contribute_upload(request, upload_code):
    """Upload panels for a reserved contribution."""
    from corpsey.apps.comics.forms import UploadForm

    message = ''
    step = 1
    page = FlatPage.objects.get(url='/contribute/upload/')
    page2 = FlatPage.objects.get(url='/contribute/upload/ok/')
    try:
        contribution = Contribution.objects.get(code=upload_code)
        parent_comic = contribution.comic
        form = UploadForm(initial = {'name': contribution.name, 'email': contribution.email})

        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                contribution.panel1 = request.FILES['panel1']
                contribution.panel2 = request.FILES['panel2']
                contribution.panel3 = request.FILES['panel3']
                contribution.name = form.cleaned_data['name']
                contribution.email = form.cleaned_data['email']
                contribution.website = form.cleaned_data['website']
                if contribution.website and not "http" in contribution.website:
                    contribution.website = 'http://%s/' % contribution.website
                contribution.has_panels = True
                contribution.save()

                message = "Contribution uploaded ok!"
                step = 2

                # Email voters about new submission
                from django.contrib.auth.models import User, Group
                mail_subject = 'New Infinite Corpse submission!'
                mail_body = 'OMG LOOK:\n\n%s\n\nGo forth Trubblers and cast your Yea or Nay: http://%s/contributions/#contribution-%s\n' % (contribution, request.META['HTTP_HOST'], contribution.id)
                voters = User.objects.filter(groups__name='voters')
                emails = ()
                # Build tuple of emails to send
                for voter in voters:
                    emails = emails + ((mail_subject, mail_body, 'hal@trubble.club', [voter.email]),)
                send_mass_mail(emails)
            else:
                message = "Oh no! Something went wrong and broke Corpsey's robot brain."
    except Contribution.DoesNotExist:
        message = 'Contribution code <strong>%s</strong> was not found!' % upload_code
        return render(request, 'comics/contribute_upload.html', {
            'message': message
        })

    if not contribution.pending:
        message = 'Contribution code <strong>%s</strong> has expired.' % upload_code
        return render(request, 'comics/contribute_upload.html', {
            'message': message
        })

    return render(request, 'comics/contribute_upload.html', {
        'upload_code': upload_code,
        'step': step,
        'contribution': contribution,
        'form': form,
        'page': page,
        'page2': page2,
        'parent_comic': parent_comic,
        'message': message
    })
