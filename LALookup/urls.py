from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from LALookup import views

urlpatterns = [
    path("", views.locateMe),
    path("contact", views.renderResposne),
    path("callMyStateRep", views.callMyStateRep),
    path("emailMyStateRep", views.emailMyStateRep),
    path("callMyStateSenator", views.callMyStateSenator),
    path("emailMyStateSenator", views.emailMyStateSenator),
    path("callMyGovernor", views.callMyGovernor),
    path("emailMyGovernor", views.emailMyGovernor),
    path("callMyGov", views.callMyGovernor),
    path("emailMyGov", views.emailMyGovernor),
    path("callMyRep", views.test),
    path("emailMyRep", views.test),
    path("emailMyMayor", views.emailMyMayor),
    path("callMyMayor", views.callMyMayor),
    path("callMyCityCouncilor", views.callMyCouncilor),
    path("emailMyCityCouncilor", views.emailMyCouncilor),
    path("stateLegislators", views.LookupStateLegislators),
    path("locateMe", views.locateMe),
    path("callSenatorCassidy", views.callSenatorCassidy),
    path("callSenatorKennedy", views.callSenatorKennedy),
    path("emailSenatorCassidy", views.emailSenatorCassidy),
    path("emailSenatorKennedy", views.emailSenatorKennedy),
    path("emailMyUSRep", views.callMyUSRep),
    path("callMyUSRep", views.callMyUSRep),
    path("campaigns", views.activeCampaigns),
    path("stats", views.stats),
    path("test", views.test),
    path("testBad", views.testBad),
    path("sitemap.txt", views.sitemap),
    # API
    path("api/test", views.apitest),
    path("api/addressSearch", views.addressSearch),
    # admin
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
