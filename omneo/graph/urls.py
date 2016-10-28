from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^datasets/', include([
        url(r'^$', views.datasets, name='main'),
        url(r'^add/$', views.add_dataset, name='add'),
        url(r'^delete/(?P<name>.+)/$', views.delete_dataset, name='delete'),
    ], namespace='datasets'))
]
