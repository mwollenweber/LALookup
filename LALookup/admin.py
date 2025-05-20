from django.contrib import admin
from .models import Legislator, SoSElectedOfficial, Request


class RequestAdmin(admin.ModelAdmin):
    model = Request
    search_fields = ['remote_address', 'response_code', 'endpoint']
    title = [Request.id, Request.method, Request.response_code]


class LegislatorAdmin(admin.ModelAdmin):
    model = Legislator
    search_fields = ['first_name', 'last_name']


class ElectedOfficialAdmin(admin.ModelAdmin):
    model = SoSElectedOfficial
    search_fields = ['first_name', 'last_name']


admin.site.register(Legislator, LegislatorAdmin)
admin.site.register(SoSElectedOfficial, ElectedOfficialAdmin)
admin.site.register(Request, RequestAdmin)