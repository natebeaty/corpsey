from django.db import models
from corpsey.apps.artists.models import Artist
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from django.conf import settings

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.cache import cache

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)

class Comic(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, null=True, blank=True, related_name='comics', on_delete=models.CASCADE)
    portal_to = models.ForeignKey('self', null=True, blank=True, related_name='portal', on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=False)
    starter = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    full_image = ThumbnailerImageField(upload_to='comics', blank=True)
    panel1 = ThumbnailerImageField(upload_to='comics', blank=True)
    panel2 = ThumbnailerImageField(upload_to='comics', blank=True)
    panel3 = ThumbnailerImageField(upload_to='comics', blank=True)

    class Meta:
        ordering = ['tree_id', 'lft']

    def get_absolute_url(self):
        if self.parent:
            return reverse('comic-entry', kwargs={'comic_1': self.parent.id, 'comic_2': self.id})
        else:
            return reverse('comic-entry-single', kwargs={'comic_1': self.id})

    def __str__(self):
        return u"%s - %s" % (self.artist, self.date.strftime('%b %d \'%y'))

    def valid_to_follow(self):
        pending_contributions = len(Contribution.objects.filter(comic_id=self.id, pending=True))
        comic_children = len(self.get_children())
        return pending_contributions + comic_children < settings.MAX_COMIC_CHILDREN

    def prev_sib(self):
        """Root nodes infinite linkage, if first, link to last"""
        if self.is_root_node() and not self.get_previous_sibling(active=True):
            return Comic.objects.root_nodes().filter(active=True).reverse()[0]
        else:
            return self.get_previous_sibling(active=True)

    def next_sib(self):
        """Root nodes infinite linkage, if last, link to first"""
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

@receiver(pre_save, sender=Comic)
def update_num_comics(sender, instance, **kwargs):
    """ Update num_comics for comic artists """
    old = Comic.objects.filter(pk=instance.pk)
    old = len(old) > 0 and old.get() or None
    if old:
        old.artist.num_comics = old.artist.num_comics - 1
        old.artist.save()
    instance.artist.num_comics = instance.artist.num_comics + 1
    instance.artist.save()

class Uturn(models.Model):
    portal_to = models.ForeignKey(Comic, related_name='uturn', on_delete=models.CASCADE)
    panel = ThumbnailerImageField(upload_to='comics', blank=True)

    def get_absolute_url(self):
        return reverse('corpsey.apps.comics.views.uturn', [str(self.id)])

    def __str__(self):
        return u"Uturn to %s" % (self.portal_to.artist)

class Contribution(models.Model):
    name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    website = models.URLField(max_length=250, blank=True)
    code = models.CharField(max_length=250, blank=True, help_text="Upload link is https://corpsey.trubble.club/contribute/upload/CODE_HERE/")
    date = models.DateTimeField(auto_now_add=True, blank=True)
    deadline = models.DateTimeField(blank=True)
    comic = models.ForeignKey(Comic, related_name='contributions', on_delete=models.CASCADE)
    panel1 = ThumbnailerImageField(upload_to='contributions', blank=True)
    panel2 = ThumbnailerImageField(upload_to='contributions', blank=True)
    panel3 = ThumbnailerImageField(upload_to='contributions', blank=True)
    pending = models.BooleanField(default=True)
    has_panels = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    # def admin_url(self):
    #     return reverse('admin:comics_contribution_change', args=[self.id])

    def votes_list(self):
        """List of votes for admin view"""
        votes_list = ''
        if self.votes:
            values = []
            for vote in self.votes.all():
                values.append(str(vote))
            votes_list = ', '.join(values)
        return votes_list

    def __str__(self):
        return u"Contribution from %s (following %s)" % (self.name, self.comic.artist)

class Rule(models.Model):
    text = models.TextField()
    def __str__(self):
        return u"%s" % self.text

class Vote(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    contribution = models.ForeignKey(Contribution, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)
    rule_broke = models.ForeignKey(Rule, null=True, blank=True, related_name='rules_broke', default=None, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        if self.approve:
            return u"Yea Vote for %s (by %s)" % (self.contribution, self.user.username)
        else:
            if self.rule_broke:
                return u"Nay Vote for %s : %s (by %s)" % (self.contribution, self.rule_broke,self.user.username)
            else:
                return u"Nay Vote for %s : %s (by %s)" % (self.contribution, self.notes, self.user.username)
