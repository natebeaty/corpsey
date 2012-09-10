from django.contrib import admin
from corpsey.apps.comics.models import Comic
from django import forms

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic

class ComicAdmin(admin.ModelAdmin):
    # list_display = ('__unicode__', 'active_toggle')
    # exclude = ['name']
    form = ComicForm

admin.site.register(Comic, ComicAdmin)