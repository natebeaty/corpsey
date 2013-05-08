from django.db import models
from corpsey.apps.artists.models import Artist
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core import urlresolvers
from datetime import datetime, timedelta
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)

# Create your models here.
class Comic(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    artist = models.ForeignKey(Artist, null=True, blank=True, related_name='comics')
    portal_to = models.ForeignKey('self', null=True, blank=True, related_name='portal')
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=False)
    starter = models.BooleanField(default=False)
    full_image = ThumbnailerImageField(upload_to='comics', blank=True)
    panel1 = ThumbnailerImageField(upload_to='comics', blank=True)
    panel2 = ThumbnailerImageField(upload_to='comics', blank=True)
    panel3 = ThumbnailerImageField(upload_to='comics', blank=True)

    class Meta:
        ordering = ['tree_id', 'lft']

    @models.permalink
    def get_absolute_url(self):
        return ('corpsey.apps.comics.views.entry', [str(self.id)])

    def __unicode__(self):
        return u"%s - %s" % (self.artist, self.date.strftime('%b %d \'%y'))
    def valid_to_follow(self):
        pending_contributions = len(Contribution.objects.filter(comic_id=self.id, pending=True))
        comic_children = len(self.get_children())
        return pending_contributions + comic_children < settings.MAX_COMIC_CHILDREN
            

    def prev_sib(self):
        # root nodes infinite linkage, if first, link to last
        if self.is_root_node() and not self.get_previous_sibling(active=True):
            return Comic.objects.root_nodes().filter(active=True).reverse()[0]
        else:
            return self.get_previous_sibling(active=True)

    def next_sib(self):
        # root nodes infinite linkage, if last, link to first
        if self.is_root_node() and not self.get_next_sibling(active=True):
            return Comic.objects.root_nodes().filter(active=True)[0]
        else:
            return self.get_next_sibling(active=True)

    def children(self):
        return self.get_children().filter(active=True)

    def get_uturn(self):
        return self.get_ancestors().all()[0].next_sib().uturn.all()

    def get_prev_comic_links(self):
        comic_links = []
        if self.is_child_node():
            comic_links.extend(self.get_ancestors(ascending=True).all()[:1])
        elif self.is_root_node() and self.prev_sib():
            comic_links.append(self.prev_sib())
        return comic_links

    def get_next_comic_links(self):
        comic_links = []
        if self.is_root_node():
            comic_links.append(self.next_sib())
        if self.children:
            comic_links.extend(self.children.all())
        if self.portal_to:
            comic_links.append(self.portal_to)

        return comic_links

@receiver(post_save, sender=Comic)
def clear_cache(sender, instance, created, **kwargs):
    """Clear homepage cache on comic save."""
    cache.delete('/')

class Uturn(models.Model):
    portal_to = models.ForeignKey(Comic, related_name='uturn')
    panel = ThumbnailerImageField(upload_to='comics', blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('corpsey.apps.comics.views.uturn', [str(self.id)])

    def __unicode__(self):
        return u"Uturn to %s" % (self.portal_to.artist)

class Contribution(models.Model):
    name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    website = models.CharField(max_length=250, blank=True)
    code = models.CharField(max_length=250, blank=True, help_text="Upload link is http://corpsey.trubbleclub.com/contribute/upload/CODE_HERE/")
    date = models.DateTimeField(auto_now_add=True, blank=True)
    deadline = models.DateTimeField(blank=True)
    comic = models.ForeignKey(Comic, related_name='contributions')
    panel1 = ThumbnailerImageField(upload_to='contributions', blank=True)
    panel2 = ThumbnailerImageField(upload_to='contributions', blank=True)
    panel3 = ThumbnailerImageField(upload_to='contributions', blank=True)
    pending = models.BooleanField(default=True)
    has_panels = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def admin_url(self):
        return urlresolvers.reverse('admin:comics_contribution_change', args=(self.id,))

    # list of votes for admin view
    def votes_list(self):
        votes_list = ''
        if self.votes:
            values = []
            for vote in self.votes.all():
                values.append(str(vote))
            votes_list = ', '.join(values)
        return votes_list

    def __unicode__(self):
        return u"Contribution from %s -- following %s" % (self.name, self.comic.artist)

class Rule(models.Model):
    text = models.TextField()
    def __unicode__(self):
        return u"%s" % self.text

class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    contribution = models.ForeignKey(Contribution, related_name='votes')
    user = models.ForeignKey(User, related_name='votes')
    approve = models.BooleanField(default=False)
    rule_broke = models.ForeignKey(Rule, null=True, blank=True, related_name='rules_broke', default=None)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        if self.approve:
            return u"Yea Vote for %s" % (self.contribution.name)
        else:
            return u"Nay Vote for %s : %s" % (self.contribution.name, self.rule_broke)
