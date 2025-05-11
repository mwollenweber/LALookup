"""
URL configuration for LALookup project.

"""

from django.contrib import admin
from django.urls import path
from LALookup import views

urlpatterns = [
    path("", views.index),
    path("test", views.test),
    path("addressSearch", views.addressSearch),
    path("contact", views.renderResposne),
    path("stateLegislators", views.LookupStateLegislators),
    path("admin/", admin.site.urls),
]
