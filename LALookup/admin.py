from django.contrib import admin
from .models import Legislator, SoSElectedOfficial, Request, Client, Campaign


class RequestAdmin(admin.ModelAdmin):
    model = Request
    search_fields = ["remote_address", "response_code", "endpoint", "date"]
    title = [Request.id, Request.method, Request.response_code, Request.date]


class LegislatorAdmin(admin.ModelAdmin):
    model = Legislator
    search_fields = ["first_name", "last_name"]


class ElectedOfficialAdmin(admin.ModelAdmin):
    model = SoSElectedOfficial
    search_fields = ["first_name", "last_name"]


class ClientAdmin(admin.ModelAdmin):
    model = Client
    search_fields = ["company_name", "email", "domain"]


class CampaignAdmin(admin.ModelAdmin):
    model = Client
    search_fields = ["client", "campaign_name"]


admin.site.register(Legislator, LegislatorAdmin)
admin.site.register(SoSElectedOfficial, ElectedOfficialAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Campaign, CampaignAdmin)
