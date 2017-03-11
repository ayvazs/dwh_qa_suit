from django.conf.urls import url
from . import views


app_name = 'dwh_qa_core'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^sync$', views.SyncView.as_view(), name = 'sync'),
    url(r'^connections$', views.ConnectionsView.as_view(), name = 'connections'),
    url(r'^connections/(?P<pk>[0-9]+)$', views.ConnectionDetailView.as_view(), name = 'connection_detail'),
    url(r'^connections/(?P<pk>[0-9]+)/update$', views.ConnectionUpdate.as_view(), name = 'connection_update'),
    url(r'^sets$', views.SetsView.as_view(), name = 'sets_view'),
    url(r'^sets/(?P<pk>[0-9]+)$', views.SetDetailView.as_view(), name = 'set_detail'),
    url(r'^sets/(?P<pk>[0-9]+)/update$', views.TestSetUpdate.as_view(), name = 'testset_update'),
    url(r'^sets/(?P<pk>[0-9]+)/tests$', views.TestsView.as_view(), name = 'tests'),
    url(r'^sets/(?P<testset_id>[0-9]+)/tests/(?P<pk>[0-9]+)$', views.TestDetailView.as_view(), name = 'test_detail'),
    url(r'^sets/(?P<testset_id>[0-9]+)/tests/(?P<pk>[0-9]+)/update$', views.TestUpdate.as_view(), name = 'test_update'),
    url(r'^sets/(?P<testset_id>[0-9]+)/tests/(?P<pk>[0-9]+)/execute$', views.TestExecute, name = 'test_execute'),
]