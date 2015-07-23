from django.conf.urls import patterns, url

urlpatterns = patterns('omnidia.views',
    url(r'^$', 'home'),
)
