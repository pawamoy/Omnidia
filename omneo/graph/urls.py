from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add, name='add'),
    # url(r'^delete/(?P<name>.+)/$', views.delete, name='delete'),
    url(r'^datasets/', include([
        # url(r'$', views.datasets, name='datasets'),
        url(r'add/', views.add_dataset, name='dataset_add'),
        url(r'delete/(?P<name>.+)/$', views.delete_dataset, name='dataset_delete'),
    ]))
]
