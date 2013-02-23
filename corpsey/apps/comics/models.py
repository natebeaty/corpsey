from django.db import models
from corpsey.apps.artists.models import Artist
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)

# Create your models here.
class Comic(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    artist = models.ForeignKey(Artist, null=True, blank=True, related_name='artists')
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

    def prev_sib(self):
        return self.get_previous_sibling(active=True)

    def next_sib(self):
        return self.get_next_sibling(active=True)

    def children(self):
        return self.get_children().filter(active=True)

    def get_prev_comic_links(self):
        comic_links = []
        # root nodes get infinite linkage, if root and first, link to last
        if self.is_root_node() and not self.prev_sib():
            comic_links.append(Comic.objects.root_nodes().reverse()[0])
        if self.is_child_node():
            comic_links.extend(self.get_ancestors(ascending=True).all()[:1])
        elif self.is_root_node() and self.prev_sib():
            comic_links.append(self.prev_sib())
        return comic_links

    def get_next_comic_links(self):
        comic_links = []
        # root nodes infinite linkage, if last, link to first
        if self.is_root_node():
            if self.next_sib():
                comic_links.append(self.next_sib())
            else:
                comic_links.append(Comic.objects.root_nodes()[0])
        if self.children:
            comic_links.extend(self.children.all())
        if self.portal_to:
            comic_links.append(self.portal_to)
        return comic_links
