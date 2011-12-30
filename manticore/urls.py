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
    HomepageView, RepinNailView,
)


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r'^$', HomepageView.as_view(), name='home'),

    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("manticore.apps.about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r"^likes/", include("phileo.urls")),

    url(r'^nail/add/$', CreateNailView.as_view(model=Nail), name='nail-add'),
    url(r'^nail/(?P<pk>\d+)/$', DetailView.as_view(model=Nail), name='nail'),
    url(r'^nail/(?P<pk>\d+)/edit/$', UpdateNailView.as_view(model=Nail), name='nail-edit'),
    url(r'^nail/(?P<pk>\d+)/delete/$', DeleteNailView.as_view(model=Nail), name='nail-delete'),
    url(r'^nail/(?P<pk>\d+)/repin/$', RepinNailView.as_view(model=Nail), name='nail-repin'),

    url(r'^workbench/add/$', CreateByView.as_view(model=Workbench), name='workbench-add'),
    url(r'^workbench/(?P<pk>\d+)/$', DetailView.as_view(model=Workbench), name='workbench'),
    url(r'^workbench/(?P<pk>\d+)/edit/$', UpdateWorkbenchView.as_view(model=Workbench), name='workbench-edit'),
    url(r'^workbench/(?P<pk>\d+)/delete/$', DeleteWorkbenchView.as_view(model=Workbench), name='workbench-delete'),

    url(r'^u/(?P<slug>\w+)/$', DetailView.as_view(model=User, slug_field='username'), name='user'),
    url(r'', include('social_auth.urls')),
)


if settings.SERVE_MEDIA:
    from staticfiles.urls import static
    urlpatterns += static(settings.STATIC_URL, view='staticfiles.views.serve')
    urlpatterns += static(settings.MEDIA_URL, view='staticfiles.views.serve')
