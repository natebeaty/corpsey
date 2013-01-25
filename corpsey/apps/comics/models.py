from django.db import models
from corpsey.apps.artists.models import Artist
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Comic(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    artist = models.ForeignKey(Artist, null=True, blank=True, related_name='artists')
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=False)
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

    # class MPTTMeta:
    #     order_insertion_by = ['date']