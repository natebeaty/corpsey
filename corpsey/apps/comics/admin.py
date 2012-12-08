from django.contrib import admin
from treeadmin.admin import TreeAdmin
from corpsey.apps.comics.models import Comic
from django import forms

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic

class ComicAdmin(TreeAdmin):
    # list_display = ('__unicode__', 'active_toggle')
    # exclude = ['name']
    form = ComicForm

admin.site.register(Comic, ComicAdmin)