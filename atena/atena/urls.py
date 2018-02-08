"""atena URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(('main.urls', 'main'), namespace='main')),
    url(r'^contas/', include(('contas.urls', 'contas'), namespace='contas')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'main.views.handler404'
handler403 = 'main.views.handler403'
handler500 = 'main.views.handler500'