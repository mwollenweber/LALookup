import time
from urllib.parse import urlparse
from .models import Request, Campaign
from .settings import IGNORED_IPS, IGNORED_UAS


class SaveRequest:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ignored_user_agents = IGNORED_UAS
        self.ignored_ips = IGNORED_IPS
        self.exclude_prefixes = ["/admin"]

    def __call__(self, request):
        _t = time.time()  # Calculated execution time.
        response = self.get_response(request)  # Get response from view function.
        _t = int((time.time() - _t) * 1000)


        if list(filter(request.get_full_path().startswith, self.exclude_prefixes)):
            return response

        if request.META.get("HTTP_USER_AGENT") in self.ignored_user_agents:
            return response

        if self.get_client_ip(request) in self.ignored_ips:
            return response

        if request.method == "POST":
            lat = request.POST["lat"] if "lat" in request.POST else None
            lon = request.POST["lon"] if "lon" in request.POST else None
            addressText = (
                request.POST["addressText"] if "addressText" in request.POST else None
            )
            campaign_id = (
                request.POST["campaignId"] if "campaignId" in request.GET else None
            )
        elif request.method == "GET":
            lat = request.GET["lat"] if "lat" in request.GET else None
            lon = request.GET["lon"] if "lon" in request.GET else None
            addressText = (
                request.GET["addressText"] if "addressText" in request.GET else None
            )
            campaign_id = (
                request.GET["campaignId"] if "campaignId" in request.GET else None
            )

        # Create instance of our model and assign values
        request_log = Request(
            endpoint=urlparse(request.get_full_path()).path,
            response_code=response.status_code,
            method=request.method,
            remote_address=self.get_client_ip(request),
            exec_time=_t,
            # body_response=str(response.content),
            # body_request=str(request.body),
            referrer=request.META.get("HTTP_REFERER"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
            lat=lat,
            lon=lon,
            addressText=addressText,
            campaign_id=campaign_id,
        )
        request_log.save()

        campaign = Campaign.objects.filter(id=campaign_id).first()
        if campaign:
            campaign.hit_count += 1
            campaign.save()

        return response

    # get clients ip address
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            _ip = x_forwarded_for.split(",")[0]
        else:
            _ip = request.META.get("REMOTE_ADDR")
        return _ip
