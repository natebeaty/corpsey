from django.contrib import admin
from treeadmin.admin import TreeAdmin
from corpsey.apps.comics.models import Comic,Uturn,Contribution,Rule,Vote
from django import forms

class ComicAdmin(TreeAdmin):
    list_display = ('__unicode__', 'active', 'starter', 'featured', 'notes')
    search_fields = ['artist__name']
    # active_toggle = tree_admin.ajax_editable_boolean('active', 'is active')
    exclude = ('full_image',)
    jquery_no_conflict = False

class UturnForm(forms.ModelForm):
    portal_to = forms.ModelChoiceField(queryset=Comic.objects.filter(lft=1))

class ContributionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pending', 'has_panels', 'accepted', 'date', 'deadline', 'votes_list')
    list_filter = ('pending', 'has_panels', 'accepted')
    search_fields = ['name', 'email']

class UturnAdmin(admin.ModelAdmin):
    form = UturnForm

class VoteAdmin(admin.ModelAdmin):
    pass

class RuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comic, ComicAdmin)
admin.site.register(Uturn, UturnAdmin)
admin.site.register(Vote, RuleAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Contribution, ContributionAdmin)