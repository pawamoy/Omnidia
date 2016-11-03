from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^datasets/', include([
        url(r'^$', views.datasets, name='main'),
        url(r'^add/$', views.dataset_add, name='add'),
        url(r'^(?P<dataset>[\w ]+)/', include([
            url(r'^$', views.dataset_details, name='details'),
            url(r'^delete/$', views.dataset_delete, name='delete'),
            url(r'^values/', include([
                url(r'^$', views.dataset_values, name='main'),
                url(r'^add/$', views.value_add, name='add'),
                url(r'^(?P<value>[\w? ]+)/', include([
                    url(r'^$', views.value_details, name='details'),
                    url(r'^delete/$', views.value_delete, name='delete'),
                ])),
            ], namespace='values'))
        ])),
    ], namespace='datasets')),
    url(r'files/', include([
        url(r'^$', views.files, name='main'),
        url(r'^(?P<path_hash>\w+)/', include([
            url(r'^delete/$', views.file_delete, name='delete'),
        ])),
    ], namespace='files'))
]
