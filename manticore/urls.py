from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic import DetailView

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer

from manticore.apps.core.models import Nail, Workbench, User
from manticore.apps.core.views import (
    CreateByView,
    UpdateWorkbenchView, DeleteWorkbenchView,
    CreateNailView, UpdateNailView, DeleteNailView,
    RenailView, AjaxAllNailsView, AjaxHomepageView
)


handler500 = "pinax.views.server_error"

from idios.views import ProfileCreateView, ProfileDetailView, ProfileUpdateView

urlpatterns = patterns("",
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/site_media/media/favicon.ico'}),

    url(r'^$', AjaxHomepageView.as_view(), name='home'),
    url(r'^all/$', AjaxAllNailsView.as_view(), name='all'),

    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("manticore.apps.about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^likes/", include("phileo.urls")),
    url(r"^comments/", include("dialogos.urls")),

    url(r'^nail/add/$', CreateNailView.as_view(model=Nail), name='nail-add'),
    url(r'^nail/(?P<pk>\d+)/$', DetailView.as_view(model=Nail), name='nail'),
    url(r'^nail/(?P<pk>\d+)/edit/$', UpdateNailView.as_view(model=Nail), name='nail-edit'),
    url(r'^nail/(?P<pk>\d+)/delete/$', DeleteNailView.as_view(model=Nail), name='nail-delete'),
    url(r'^nail/(?P<pk>\d+)/renail/$', RenailView.as_view(model=Nail), name='nail-renail'),

    url(r'^workbench/add/$', CreateByView.as_view(model=Workbench), name='workbench-add'),
    url(r'^workbench/(?P<pk>\d+)/$', DetailView.as_view(model=Workbench), name='workbench'),
    url(r'^workbench/(?P<pk>\d+)/edit/$', UpdateWorkbenchView.as_view(model=Workbench), name='workbench-edit'),
    url(r'^workbench/(?P<pk>\d+)/delete/$', DeleteWorkbenchView.as_view(model=Workbench), name='workbench-delete'),

    url(r'^u/(?P<slug>[\w\._-]+)/$', DetailView.as_view(model=User, slug_field='username'), name='user'),
    url(r"^u/(?P<username>[\w\._-]+)/profile/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r"^edit/$", ProfileUpdateView.as_view(), name="profile_edit"),
    url(r"^create/$", ProfileCreateView.as_view(), name="profile_create"),

    url(r'^search/', include('haystack.urls')),

    url(r'^', include('social_auth.urls')),
    url(r'^', include('follow.urls')),
)


if settings.SERVE_MEDIA:
    from staticfiles.urls import static
    urlpatterns += static(settings.STATIC_URL, view='staticfiles.views.serve')
    urlpatterns += static(settings.MEDIA_URL, view='staticfiles.views.serve')
