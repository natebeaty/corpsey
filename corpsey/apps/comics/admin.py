from django.contrib import admin
# from treeadmin import admin as tree_admin
from treeadmin.admin import TreeAdmin
from corpsey.apps.comics.models import Comic,Uturn,Contribution
from django import forms

class ComicAdmin(TreeAdmin):
    list_display = ('__unicode__', 'active', 'starter', 'notes')
    # active_toggle = tree_admin.ajax_editable_boolean('active', 'is active')
    exclude = ('full_image',)

class UturnForm(forms.ModelForm):
    portal_to = forms.ModelChoiceField(queryset=Comic.objects.filter(lft=1))

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pending', 'accepted', 'deadline', 'notes')

class UturnAdmin(admin.ModelAdmin):
	form = UturnForm

admin.site.register(Comic, ComicAdmin)
admin.site.register(Uturn, UturnAdmin)
admin.site.register(Contribution, ContributionAdmin)