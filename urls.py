from django.conf.urls import url
from .import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^list/$', views.TicketView.as_view(), name='list'),
    url(r'^pending/$', views.PendingTicketView.as_view(), name='pending'),
    url(r'^solved/$', views.SolvedTicketView.as_view(), name='solved'),
    url(r'^reopened/$', views.ReopenedTicketView.as_view(), name='reopened'),
    url(r'^closed/$', views.ClosedTicketView.as_view(), name='closed'),
    url(r'^(?P<pk>\d+)/detail/$', views.TicketDetailView.as_view(),
        name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.TicketupdateView.as_view(),
        name='update'),
    url(r'^(?P<pk>\d+)/comment/$', views.TicketCommentView.as_view(),
        name='comment'),
    url(r'^$', 'django.contrib.auth.views.login',
        {'template_name': 'base_login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'base_login.html'}, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)