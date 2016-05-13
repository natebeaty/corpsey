from corpsey.apps.comics.models import *
from dajaxice.decorators import dajaxice_register
from easy_thumbnails.files import get_thumbnailer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import json
import twitter
import random

def get_uturn_panel(request, uturn_id, direction, hdpi_enabled):
    """The wacky uturn anomaly that turned Nate super bald."""
    uturn = Uturn.objects.get(pk=uturn_id)
    size = 'midsize_hd' if hdpi_enabled else 'midsize'
    if uturn:
        uturn_obj = {
            'panel' : get_thumbnailer(uturn.panel)[size].url, 
            'uturn_id' : uturn.id,
            'portal_to_id' : uturn.portal_to.id,
        }
    else:
        uturn_obj = {}

    return json.dumps({ 
        'direction' : direction,
        'uturn' : uturn_obj
    })

def get_comic_panels(request, comic_id, direction, hdpi_enabled):
    """Ajaxtastic catacombs browsing magic."""
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

    # store comic_id for /contribute/
    request.session['last_comic_id'] = comic_id

    return json.dumps({ 
        'direction' : direction,
        'comic' : comic_obj
    })

def contribution_vote(request, contribution_id, yea, rule_broke=0, notes=''):
    """The elders voting YAY OR NAY on freshly contributed strips."""
    contribution = Contribution.objects.get(pk=contribution_id)
    # has this already been approved?
    if contribution.pending == False:
        return json.dumps({ 
            'message' : "This contribution is not in the queue any longer."
        })
    approve = True if yea == 1 else False
    message = ''

    if rule_broke == 0:
        rule_broke = None
    else:
        rule_broke = Rule.objects.get(pk=rule_broke)

    vote = Vote(
        contribution = contribution,
        user = request.user,
        approve = approve,
        rule_broke = rule_broke,
        notes = notes,
        )
    vote.save()

    """Count votes and if 2 Nay or 2 Yea have been reached, take action."""

    num_yea_votes = len(contribution.votes.filter(approve=True))
    num_nay_votes = len(contribution.votes.filter(approve=False))

    # reject contribution
    if num_nay_votes > 2:
        contribution.pending = False
        contribution.save()
        # email user that their comic was rejected
        plaintext = get_template('emails/contribution_rejected.txt')
        htmly     = get_template('emails/contribution_rejected.html')

        d = Context({ 
            'votes': contribution.votes.filter(approve=False),
            'parent_id': contribution.comic.id,
            'name': contribution.name,
            })

        subject, from_email, to = 'Your Infinite Corpse contribution', 'corpsey@trubbleclub.com', contribution.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            message = 'There was an error sending the rejection email to %s. Please write Nate and mock him.' % contribution.email

    # approve contribution
    if num_yea_votes > 2:
        contribution.pending = False
        contribution.accepted = True
        contribution.save()
        # look for artist or add new
        try:
            artist = Artist.objects.get(name=contribution.name)
        except:
            artist = Artist(name=contribution.name)
        artist.email = contribution.email
        artist.url = contribution.website
        artist.save()

        comic = Comic(
            artist = artist,
            active = True,
            parent = contribution.comic,
            panel1 = contribution.panel1,
            panel2 = contribution.panel2,
            panel3 = contribution.panel3,
        )
        comic.save()
        # email user that their comic was approved
        plaintext = get_template('emails/contribution_approved.txt')
        htmly     = get_template('emails/contribution_approved.html')

        d = Context({ 
            'comic_url': "/catacombs/%s/%s/" % (contribution.comic.id, comic.id),
            'comic': comic,
            'name': contribution.name,
            })

        subject, from_email, to = 'Your Infinite Corpse contribution is live!', 'corpsey@trubbleclub.com', contribution.email
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            message = 'There was an error sending the approval email to %s. Please write Nate and mock him.' % contribution.email

        # post link to twitter
        phrase = random.choice(
            (
                'New panels posted by',
                'The catacombs are chattering with panels by',
                'What\'s this? New panels by',
                'And you don\'t stop, new panels by',
                'You better believe it, new panels by',
                'Hey-oh! Fresh panels by',
                'Hot diggety! New panels by',
                'Holy smokes, new panels by',
                'Stop the presses! new panels by',
                'Ain\'t no half steppin\', new panels by',
                'Fresh panels in the catacombs by',
                'Oh look! Brand new panels by',
                'Shazam! Panels by',
                'This just keeps getting better. New panels by',
            )
        )
        twitter_api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY, consumer_secret=settings.TWITTER_CONSUMER_SECRET, access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY, access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
        try:
            twitter_api.PostUpdate("%s %s, following %s: http://%s/catacombs/%s/%s/" % (phrase, comic.artist, comic.parent.artist, request.META['HTTP_HOST'], comic.parent.id, comic.id))
        except:
            message = 'There was an error posting to twitter. Please write Nate and mock him.'

    return json.dumps({ 
        'contribution_id' : contribution_id,
        'yea' : yea,
        'message' : message
    })

def get_new_leaf(request, comic_id, hdpi_enabled):
    """Pull another random strip to follow for /contribute/ page."""
    from corpsey.apps.comics.views import find_comic_to_follow
    comic = find_comic_to_follow(comic_id)
    size = 'midsize_hd' if hdpi_enabled else 'midsize'
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
    return json.dumps({ 
        'comic' : comic_obj
    })

def get_nav_links(request, comic_id_arr, is_uturn):
    """Ajaxtastic next/prev links, overly verbose at the moment just so they work."""
    next_comic_links_arr = []
    prev_comic_links_arr = []
    uturn_links = []

    if is_uturn:
        uturn = Uturn.objects.get(pk=comic_id_arr[0])
        # /catacombs/uturn/uturn_id/ (comic_id_arr[1] is sent along by js magic, taken from uturn's data-portal-id)
        if comic_id_arr[1] == uturn.portal_to.id:
            next_comic_links = uturn.portal_to.get_next_comic_links()
            if next_comic_links:
                for link in next_comic_links:
                    next_comic_links_arr.append({ 
                        'comic_id': link.id, 
                        'comic_id_2': uturn.portal_to.id,
                        'artist_name': link.artist.name, 
                        'artist_name_2': uturn.portal_to.artist.name, 
                        'first_name': link.artist.first_name, 
                        'last_name': link.artist.last_name, 
                        'name': link.artist.name, 
                    })
        else:
            # /catacombs/uturn/uturn_id/comic that's not the portal!
            comic = Comic.objects.get(pk=comic_id_arr[1])
            prev_comic_links = comic.get_prev_comic_links()
            if prev_comic_links:
                for link in prev_comic_links:
                    prev_comic_links_arr.append({ 
                        'comic_id': link.id, 
                        'comic_id_2': comic.id,
                        'artist_name': link.artist.name, 
                        'artist_name_2': comic.artist.name, 
                        'first_name': link.artist.first_name, 
                        'last_name': link.artist.last_name, 
                        'name': link.artist.name, 
                    })
            uturn_links = [{
                'uturn_id': uturn.id,
                'comic_id': '',
                'artist_name': 'Trubble Club', 
                'artist_name_2': uturn.portal_to.artist.name, 
                'first_name': uturn.portal_to.artist.first_name,
                'last_name': uturn.portal_to.artist.last_name,
                }]

    else:
        comic = Comic.objects.get(pk=comic_id_arr[0])
        prev_comic_links = comic.get_prev_comic_links()
        if prev_comic_links:
            for link in prev_comic_links:
                prev_comic_links_arr.append({ 
                    'comic_id': link.id, 
                    'comic_id_2': comic.id,
                    'artist_name': link.artist.name, 
                    'artist_name_2': comic.artist.name, 
                    'first_name': link.artist.first_name, 
                    'last_name': link.artist.last_name, 
                    'name': link.artist.name, 
                })

        if len(comic_id_arr) == 1:
            comic = Comic.objects.get(pk=comic_id_arr[0])
        else:
            comic = Comic.objects.get(pk=comic_id_arr[1])

        next_comic_links = comic.get_next_comic_links()
        if next_comic_links:
            for link in next_comic_links:
                next_comic_links_arr.append({ 
                    'comic_id': link.id, 
                    'comic_id_2': comic.id,
                    'artist_name': link.artist.name, 
                    'artist_name_2': comic.artist.name, 
                    'first_name': link.artist.first_name, 
                    'last_name': link.artist.last_name, 
                    'name': link.artist.name, 
                })
        else:
            if comic.is_child_node:
                uturn = comic.get_uturn()
                if (uturn):
                    uturn_links = [{
                        'uturn_id': uturn[0].id,
                        'comic_id': comic.id,
                        'artist_name': 'Trubble Club', 
                        'artist_name_2': uturn[0].portal_to.artist.name, 
                        'first_name': 'Trubble',
                        'last_name': 'Club',
                    }]

    return json.dumps({ 
        'prev_comic_links' : prev_comic_links_arr,
        'next_comic_links' : next_comic_links_arr,
        'uturn_links' : uturn_links,
    })
