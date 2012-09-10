from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True)
    image = ThumbnailerImageField(upload_to='artists', blank=True)
    
    def __unicode__(self):
        return self.name
