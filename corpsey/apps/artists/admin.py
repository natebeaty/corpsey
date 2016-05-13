from django.contrib import admin
from corpsey.apps.artists.models import Artist
from django import forms

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = '__all__'

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'url')
    search_fields = ['name']
    # exclude = ['first_name','last_name']
    form = ArtistForm

admin.site.register(Artist, ArtistAdmin)