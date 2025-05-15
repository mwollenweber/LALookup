"""
URL configuration for LALookup project.

"""

from django.contrib import admin
from django.urls import path
from LALookup import views

urlpatterns = [
    # index
    path("", views.index),
    # WEB
    path("contact", views.renderResposne),
    path("callMyStateRep", views.callMyStateRep),
    path("emailMyStateRep", views.emailMyStateRep),
    path("callMyStateSenator", views.callMyStateSenator),
    path("emailMyStateSenator", views.emailMyStateSenator),
    path("callMyGovernor", views.test),
    path("emailMyGovernor", views.test),
    path("callMyRep", views.test),
    path("emailMyRep", views.test),
    path("emailMyMayor", views.test),
    path("callMyMayor", views.test),
    path("stateLegislators", views.LookupStateLegislators),
    path("locateMe", views.locateMe),
    path("test", views.test),
    # path("redirect", views.redirect),
    # API
    path("api/test", views.apitest),
    path("api/addressSearch", views.addressSearch),
    # admin
    path("admin/", admin.site.urls),
]
