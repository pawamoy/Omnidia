from django.conf.urls import url, include
from django.contrib import admin
from watchdog.observers import Observer
from core.settings import MEDIA_ROOT
from omnidia.watcher import OmnidiaEventHandler
from omnidia import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', views.home, name='home'),
]

urlpatterns += [
    url(r'^$', views.home),
]

observer = Observer()
observer.schedule(OmnidiaEventHandler(), path=MEDIA_ROOT, recursive=True)
observer.start()
