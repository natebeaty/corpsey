from django.urls import include, re_path
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
    re_path(r'^$', views.home, name='home'),
    re_path(r'^artists/$', artists_views.artists, name='artists'),
    re_path(r'^artist/([\d]+)/$', artists_views.entry, name='artist'),
    re_path(r'^about/$', views.about, name='about'),

    re_path(r'^catacombs/featured/$', comics_views.featured, name='featured'),
    re_path(r'^catacombs/uturn/(?P<uturn>[\d]+)/(?P<comic>\d+)/$', comics_views.uturn, name='comic-uturn'),
    re_path(r'^catacombs/uturn/(?P<uturn>[\d]+)/$', comics_views.uturn, name='comic-uturn-single'),
    re_path(r'^catacombs/(?P<comic_1>[\d]+)/(?P<comic_2>\d+)/$', comics_views.entry, name='comic-entry'),
    re_path(r'^catacombs/(?P<comic_1>[\d]+)/$', comics_views.entry, name='comic-entry-single'),
    re_path(r'^catacombs/$', lambda x: redirect('/')),
    re_path(r'^random/$', comics_views.random_comic, name='random-comic'),
    re_path(r'^enter_the_catacombs/$', comics_views.enter_the_catacombs, name='enter-the-catacombs'),
    re_path(r'^tree/$', comics_views.tree, name='tree'),
    re_path(r'^tree_css/$', comics_views.tree_css, name='tree-css'),
    re_path(r'^tree_circle/$', comics_views.tree_circle, name='tree-circle'),
    re_path(r'^tree_json/$', comics_views.tree_json, name='tree-json'),
    re_path(r'^artist_in_catacombs/(?P<artist>\d+)/(?P<num>\d+)/$', comics_views.artist_in_catacombs, name='artist-in-catacombs'),

    re_path(r'^contribute/upload/(?P<upload_code>[\w\-=_]+)/$', comics_views.contribute_upload, name='contribute-upload'),
    re_path(r'^contribute/upload/$', lambda x: redirect('/')),
    re_path(r'^contribute/$', comics_views.contribute, name='contribute'),
    re_path(r'^contribution_vote/$', comics_ajax.contribution_vote),
    re_path(r'^pad_panels/(?P<contribution>[\d]+)/$', comics_views.pad_panels, name='pad'),

    re_path(r'^contributions/$', comics_views.contributions, name='contributions'),
    re_path(r'^graveyard/$', comics_views.graveyard, name='graveyard'),

    re_path(r'^user/login/$', auth_views.LoginView.as_view(), name='user-login'),
    re_path(r'^user/logout/$', views.logout_view, name='user-logout'),
    re_path(r'^user/password/reset/$',
        auth_views.PasswordResetView.as_view(),
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name='password_reset'),
    re_path(r'^user/password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    re_path(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(),
        {'post_reset_redirect' : '/user/password/done/'},
        name='password_reset_confirm'),
    re_path(r'^user/password/done/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    # AJAX
    re_path(r'^ajax/get_comic_panels/$', comics_ajax.get_comic_panels),
    re_path(r'^ajax/get_uturn_panel/$', comics_ajax.get_uturn_panel),
    re_path(r'^ajax/get_nav_links/$', comics_ajax.get_nav_links),
    re_path(r'^ajax/get_new_leaf/$', comics_ajax.get_new_leaf),
    re_path(r'^ajax/load_more/$', comics_ajax.load_more),

    # Django and apps
    re_path(r'^admin/clearcache/', include('clearcache.urls')),
    re_path(r'^admin/', admin.site.urls),
    # re_path(r'^markitup/', markitup.urls),
    re_path(r'^media/(?P<path>.*)$', django_views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]
