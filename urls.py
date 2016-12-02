from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^coldlist/$', views.ColdCallContactView.as_view(), name="coldlist"),
    url(r'^coldcallform/$', views.ModalCreateView.as_view(), name="coldcallform"),
    url(r'^detail/(?P<pk>\d+)/$', views.ColdCallContactDetailView.as_view(),
        name='colodetail'),
    url(r'^update/(?P<pk>\d+)/$', views.ColdCallContactUpdateView.as_view(),
        name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.DeletecoldcallCommunicationView.as_view(),
        name='delete'),
    url(r'^(?P<pk>\d+)/communication/$', views.CommunicationView.as_view(),
        name='communication'),
    url(r'^move_to_crm/$', views.MoveToCrmView.as_view(), name="move_to_crm"),
]
