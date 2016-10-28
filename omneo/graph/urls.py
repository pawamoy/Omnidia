from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^datasets/', include([
        url(r'^$', views.datasets, name='main'),
        url(r'^(?P<name>.+)/', include([
            url(r'^$', views.detail_dataset, name='details'),
            url(r'^values/', include([
                url(r'^$', views.dataset_values, name='main'),
                url(r'^(?P<name>.+)/', include([
                    url(r'^$', views.detail_dataset_value, name='details'),
                    url(r'^add/$')
                ])),
            ], namespace='values'))
        ])),
        url(r'^add/$', views.add_dataset, name='add'),
        url(r'^delete/(?P<name>.+)/$', views.delete_dataset, name='delete'),
    ], namespace='datasets')),
]
