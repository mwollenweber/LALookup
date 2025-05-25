import time
from .models import Request, Campaign


class SaveRequest:
    def __init__(self, get_response):
        self.get_response = get_response

        # Filter to log all request to url's that start with any of the strings below.
        # With example below:
        # /example/test/ will be logged.
        # /other/ will not be logged.
        self.prefixs = ["/"]

        self.exclude_prefixes = ["/admin"]

    def __call__(self, request):
        _t = time.time()  # Calculated execution time.
        response = self.get_response(request)  # Get response from view function.
        _t = int((time.time() - _t) * 1000)

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        # (Remove these two lines below to log everything)
        # if not list(filter(request.get_full_path().startswith, self.prefixs)):
        #     return response

        if list(filter(request.get_full_path().startswith, self.exclude_prefixes)):
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
            endpoint=request.get_full_path(),
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

        campaign = Campaign.objects.filter(campaign_id=campaign_id).first()
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
