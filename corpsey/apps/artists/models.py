from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
import re

class Artist(models.Model):
    name = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    url = models.URLField(max_length=250, blank=True)
    image = ThumbnailerImageField(upload_to='artists', blank=True)
    num_comics = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def name_reversed(self):
        if self.last_name and self.first_name:
            return "%s, %s" % (self.last_name, self.first_name)
        else:
            return self.name

    def update_num_comics(self):
        self.num_comics = self.comics.count()
        self.save()

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('artist', args=[self.id])

    def save(self, *args, **kwargs):
        # generate first/last name from full name
        if self.name and not self.first_name and not self.last_name:
            foo = self.name.split(' ');
            self.last_name = foo[-1]
            self.first_name = re.sub(foo[-1], "",self.name).strip()
        super(Artist, self).save(*args, **kwargs)

@receiver(post_save, sender=Artist)
def clear_cache(sender, instance, created, **kwargs):
    """Clear artists page cache on artist save."""
    cache.delete('/artists/')
