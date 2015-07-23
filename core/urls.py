from django.conf.urls import url, include
from django.contrib import admin
from watchdog.observers import Observer
from core.settings import MEDIA_ROOT
from omnidia.watcher import OmnidiaEventHandler

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'omnidia.views.home', name='home'),
]

urlpatterns += [
    url(r'^$', 'omnidia.views.home'),
]

observer = Observer()
observer.schedule(OmnidiaEventHandler(), path=MEDIA_ROOT, recursive=True)
observer.start()
