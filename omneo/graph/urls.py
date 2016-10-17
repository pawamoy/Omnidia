from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.persons, name='persons'),
    url(r'^persons/$', views.persons, name='persons'),
    url(r'^add_person/(?P<person>\w+)/$', views.add_person, name='add_person'),
    url(r'^search_persons/(?P<name>\w+)/$', views.search_persons, name='search_persons')
]
