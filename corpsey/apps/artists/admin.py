from django.contrib import admin
from corpsey.apps.artists.models import Artist
from django import forms

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist

class ArtistAdmin(admin.ModelAdmin):
    # list_display = ('__unicode__', 'active_toggle')
    # exclude = ['name']
    form = ArtistForm

admin.site.register(Artist, ArtistAdmin)