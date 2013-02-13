from django.contrib import admin
# from treeadmin import admin as tree_admin
from treeadmin.admin import TreeAdmin
from corpsey.apps.comics.models import Comic
from django import forms

class ComicAdmin(TreeAdmin):
    list_display = ('__unicode__', 'active', 'starter')
    # active_toggle = tree_admin.ajax_editable_boolean('active', 'is active')
    exclude = ('full_image',)

admin.site.register(Comic, ComicAdmin)