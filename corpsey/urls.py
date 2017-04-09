from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.shortcuts import redirect
from . import views
from corpsey.apps.comics import views as comics_views
from corpsey.apps.comics import ajax as comics_ajax
from corpsey.apps.artists import views as artists_views
from django.contrib.auth import views as auth_views
from django import views as django_views
from django.contrib import admin
admin.autodiscover()
admin.site.site_header = 'Infinitely Corpsey'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^artists/$', artists_views.artists, name='artists'),
    url(r'^artist/([\d]+)/$', artists_views.entry, name='artist'),
    url(r'^about/$', views.about, name='about'),

    url(r'^catacombs/featured/$', comics_views.featured, name='featured'),
    url(r'^catacombs/uturn/(?P<uturn>[\d]+)/(?P<comic>\d+)/$', comics_views.uturn, name='comic-uturn'),
    url(r'^catacombs/uturn/(?P<uturn>[\d]+)/$', comics_views.uturn, name='comic-uturn-single'),
    url(r'^catacombs/(?P<comic_1>[\d]+)/(?P<comic_2>\d+)/$', comics_views.entry, name='comic-entry'),
    url(r'^catacombs/(?P<comic_1>[\d]+)/$', comics_views.entry, name='comic-entry-single'),
    url(r'^catacombs/$', lambda x: redirect('/')),
    url(r'^random/$', comics_views.random, name='random-comic'),
    url(r'^enter_the_catacombs/$', comics_views.enter_the_catacombs, name='enter-the-catacombs'),
    url(r'^tree/$', comics_views.tree, name='tree'),
    url(r'^tree_css/$', comics_views.tree_css, name='tree-css'),
    url(r'^tree_json/$', comics_views.tree_json, name='tree-json'),
    url(r'^artist_in_catacombs/(?P<artist>\d+)/(?P<num>\d+)/$', comics_views.artist_in_catacombs, name='artist-in-catacombs'),

    url(r'^contribute/upload/(?P<upload_code>[\w\-=_]+)/$', comics_views.contribute_upload, name='contribute-upload'),
    url(r'^contribute/upload/$', lambda x: redirect('/')),
    url(r'^contribute/$', comics_views.contribute, name='contribute'),
    url(r'^contribution_vote/$', comics_ajax.contribution_vote),
    url(r'^pad_panels/(?P<contribution>[\d]+)/$', comics_views.pad_panels, name='pad'),

    url(r'^contributions/$', comics_views.contributions, name='contributions'),
    url(r'^graveyard/$', comics_views.graveyard, name='graveyard'),

    url(r'^user/login/$', auth_views.login, name='user-login'),
    url(r'^user/logout/$', views.logout_view, name='user-logout'),
    url(r'^user/password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        auth_views.password_reset_done),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$',
        auth_views.password_reset_complete),

    # AJAX
    url(r'^ajax/get_comic_panels/$', comics_ajax.get_comic_panels),
    url(r'^ajax/get_uturn_panel/$', comics_ajax.get_uturn_panel),
    url(r'^ajax/get_nav_links/$', comics_ajax.get_nav_links),
    url(r'^ajax/get_new_leaf/$', comics_ajax.get_new_leaf),
    url(r'^ajax/load_more/$', comics_ajax.load_more),

    # Django and apps
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markitup/', include('markitup.urls')),
    url(r'^media/(?P<path>.*)$', django_views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]
