"""
URL configuration for LALookup project.

"""

from django.contrib import admin
from django.urls import path
from LALookup import views

urlpatterns = [
    # index
    path("", views.locateMe),
    # WEB
    path("contact", views.renderResposne),
    path("callMyStateRep", views.callMyStateRep),
    path("emailMyStateRep", views.emailMyStateRep),
    path("callMyStateSenator", views.callMyStateSenator),
    path("emailMyStateSenator", views.emailMyStateSenator),
    path("callMyGovernor", views.callMyGovernor),
    path("emailMyGovernor", views.emailMyGovernor),
    path("callMyRep", views.test),
    path("emailMyRep", views.test),
    path("emailMyMayor", views.emailMyMayor),
    path("callMyMayor", views.callMyMayor),
    path("stateLegislators", views.LookupStateLegislators),
    path("callMyUSRep", views.callMyUSRep),
    path("locateMe", views.locateMe),
    path("test", views.test),
    # API
    path("api/test", views.apitest),
    path("api/addressSearch", views.addressSearch),
    # admin
    path("admin/", admin.site.urls),
]
