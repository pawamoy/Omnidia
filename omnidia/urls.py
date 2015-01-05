from django.conf.urls import patterns, include, url

urlpatterns = patterns('model.views',
    url(r'^home/', 'home'),
)
