"""
URL configuration for LALookup project.

"""

from django.contrib import admin
from django.urls import path
from LALookup import views

urlpatterns = [
    #index
    path("", views.index),

    #WEB
    path("contact", views.renderResposne),
    path("callMyRep", views.callMyRep),
    path("stateLegislators", views.LookupStateLegislators),
    path("locateMe", views.locateMe),
    path("test", views.test),


    #API
    path("api/test", views.apitest),
    path("api/addressSearch", views.addressSearch),

    #admin
    path("admin/", admin.site.urls),
]
