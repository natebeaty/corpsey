from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'corpsey.views.home', name='home'),
    url(r'^artists/$', 'corpsey.views.artists', name='artists'),
    url(r'^about/$', 'corpsey.views.about', name='about'),
    url(r'^catacombs/uturn/(?P<uturn>[\d]+)/(?P<comic>\d+)/$', 'corpsey.apps.comics.views.uturn', name='uturn'),
    url(r'^catacombs/uturn/(?P<uturn>[\d]+)/$', 'corpsey.apps.comics.views.uturn', name='uturn'),
    url(r'^catacombs/(?P<comic_1>[\d]+)/(?P<comic_2>\d+)/$', 'corpsey.apps.comics.views.entry', name='comic'),
    url(r'^catacombs/(?P<comic_1>[\d]+)/$', 'corpsey.apps.comics.views.entry', name='comic'),
    url(r'^catacombs/$', lambda x: redirect('/')),
    url(r'^random/$', 'corpsey.apps.comics.views.random', name='random'),
    url(r'^random_starter/$', 'corpsey.apps.comics.views.random_starter', name='random_starter'),
    url(r'^tree/$', 'corpsey.apps.comics.views.tree', name='tree'),
    url(r'^tree_json/$', 'corpsey.apps.comics.views.tree_json', name='tree_json'),
    url(r'^artist_in_catacombs/(?P<artist>\d+)/$', 'corpsey.apps.comics.views.artist_in_catacombs', name='artists_in_catacombs'),
    url(r'^contribute/upload/(?P<upload_code>[\w\-=_]+)/$', 'corpsey.apps.comics.views.contribute_upload', name='contribute_upload'),
    url(r'^contribute/upload/$', lambda x: redirect('/')),
    url(r'^contribute/$', 'corpsey.apps.comics.views.contribute', name='contribute'),
    url(r'^contributions/$', 'corpsey.apps.comics.views.contributions', name='contributions'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # url(r'^contributions/vote/(?P<contribution_id>[\d]+)/(?P<vote>[\d]+)/$', 'corpsey.apps.comics.views.contribution_vote', name='contribution_vote'),
    
    url(r'^artist/([\d]+)/$', 'corpsey.apps.artists.views.entry', name='artist'),
    url(r'^get_artists/$', 'corpsey.apps.artists.views.get_artists', name='get_artists'),
            
    # url(r'^admin/filebrowser/', include(site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^grappelli/', include('grappelli.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    url(r'^markitup/', include('markitup.urls')),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()