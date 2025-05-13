"""
URL configuration for LALookup project.

"""

from django.contrib import admin
from django.urls import path
from LALookup import views

urlpatterns = [
    path("", views.index),
    path("api/test", views.test),
    path("api/addressSearch", views.addressSearch),
    path("contact", views.renderResposne),
    path("stateLegislators", views.LookupStateLegislators),
    path("locateMe", views.locateMe),
    path("admin/", admin.site.urls),
]
