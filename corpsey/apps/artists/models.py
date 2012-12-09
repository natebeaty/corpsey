from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
import re 

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True)
    image = ThumbnailerImageField(upload_to='artists', blank=True)
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('artist.views.entry', [str(self.slug)])

    def save(self, *args, **kwargs):
		# generate first/last name from full name
        if self.name and not self.first_name and not self.last_name:
			foo = self.name.split(' ');
			self.last_name = foo[-1]
			self.first_name = re.sub(foo[-1], "",self.name).strip()
        super(Artist, self).save(*args, **kwargs)
