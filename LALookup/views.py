import logging
from urllib.parse import unquote
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.template import loader
from .lalookup import (
    address2latlon,
    getStateRep,
    getStateSenator,
    getGovernor,
    getMayor,
    getElectedOfficials,
    getUSRep,
    getLocation,
    locationIsValid,
    getSenatorCassidy,
    getSenatorKennedy,
    getContext,
    getActiveCampaigns,
    getCityCouncilor,
    getPageStats,
)


logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def sitemap(request):
    base_url = f"https://{request.get_host()}"
    urls = [
        f"{base_url}/locateMe\n",
        f"{base_url}/callMyStateRep\n",
        f"{base_url}/emailMyStateRep\n",
        f"{base_url}/callMyStateSenator\n",
        f"{base_url}/emailMyStateSenator\n",
        f"{base_url}/callMyGovernor\n",
        f"{base_url}/emailMyGovernor\n",
        f"{base_url}/callMyGovernor\n",
        f"{base_url}/emailMyGovernor\n",
        f"{base_url}/callMyMayor\n",
        f"{base_url}/emailMyMayor\n",
        f"{base_url}/callCityCouncilor\n",
        f"{base_url}/emailMyCityCouncilor\n",
        f"{base_url}/callMyUSRep\n",
        f"{base_url}/emailMyUSRep\n",
        f"{base_url}/api/adddressSearch\n",
        f"{base_url}/callSenatorCassidy\n",
        f"{base_url}/callSenatorKennedy\n",
        f"{base_url}/emailSenatorCassidy\n",
        f"{base_url}/emailSenatorKennedy\n",
        f"{base_url}/campaigns\n",
    ]
    return HttpResponse(urls, content_type="text/plain")


@login_required
@require_http_methods(["GET"])
def activeCampaigns(request):
    template = loader.get_template("campaigns.html")
    context = {
        "campaigns": getActiveCampaigns(),
    }
    return HttpResponse(template.render(context, request))


@login_required
@require_http_methods(["GET"])
def stats(request):
    template = loader.get_template("stats.html")
    context = {"page_stats": getPageStats()}
    return HttpResponse(template.render(context, request))


@require_http_methods(["POST", "GET"])
def addressSearch(request):
    if "lat" in request.POST.keys() and "lon" in request.POST.keys():
        lat = request.POST["lat"]
        lon = request.POST["lon"]
    elif "address" in request.POST.keys():
        address = unquote(request.POST["address"])
        lat, lon = address2latlon(address)
    elif "lat" in request.GET.keys() and "lon" in request.GET.keys():
        lat = request.GET["lat"]
        lon = request.GET["lon"]
    elif "address" in request.GET.keys():
        address = request.GET["address"]
        lat, lon = address2latlon(address)
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": f"You must provide an address or lat and lon",
            }
        )
    location = getLocation(lat, lon)
    response = {
        "status": "success",
        "address": location["address"],
        "lat": location["lat"],
        "lon": location["lon"],
        "parish": location["county"],
        "state": location["state"],
        "results": getElectedOfficials(location),
    }
    return JsonResponse(response)


@require_http_methods(["GET"])
def locateMe(request):
    template = loader.get_template("search.html")
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyStateRep(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getStateRep(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Louisiana State Representative"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyStateRep(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getStateRep(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Louisiana State Representative"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyCouncilor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getCityCouncilor(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Council Person"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyCouncilor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getCityCouncilor(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Council Person"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyUSRep(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getUSRep(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your US Representative"
        context["target_url"] = target_url
        context["results"] = [official]

        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyUSRep(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getUSRep(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your US Representative"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyStateSenator(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getStateSenator(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your State Senator"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyStateSenator(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getStateSenator(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your State Senator"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyMayor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getMayor(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Mayor"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyMayor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getMayor(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Mayor"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def callMyGovernor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getGovernor(location)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Governor"
        context["target_url"] = target_url
        context["results"] = [official]
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def emailMyGovernor(request):
    if request.method == "POST":
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        location = getLocation(lat, lon)
        if not locationIsValid(location):
            return invalidState(request)
        official = getGovernor(location)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = getContext(request)
        context["header"] = "Your Governor"
        context["target_url"] = target_url
        context["results"] = [official]

        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


def apitest(request):
    address = "4521 Magazine St, 70115"
    lat, lon = address2latlon(address)
    location = getLocation(lat, lon)
    r = {
        "status": "success",
        "address": address,
        "lat": lat,
        "lon": lon,
        "parish": location["county"],
        "results": getElectedOfficials(location),
    }
    return JsonResponse(r)


def test(request):
    address = "4521 Magazine St, 70115"
    lat, lon = address2latlon(address)
    location = getLocation(lat, lon)
    if not locationIsValid(location):
        return invalidState(request)
    logger.info(f"render body: {request.body}")
    template = loader.get_template("contact.html")
    results = getElectedOfficials(location)
    for r in results:
        logger.debug(f"test result: {r}")
    context = {"results": results}
    context["title"] = "TEST"
    return HttpResponse(template.render(context, request))


def testBad(request):
    address = "9600 N. MoPac Expressway,  78759"
    lat, lon = address2latlon(address)
    location = getLocation(lat, lon)
    if not locationIsValid(location):
        return invalidState(request)
    logger.info(f"render body: {request.body}")
    template = loader.get_template("contact.html")
    results = getElectedOfficials(location)
    for r in results:
        logger.debug(f"test result: {r}")
    context = {"results": results}
    context["title"] = "TEST BAD"
    return HttpResponse(template.render(context, request))


def LookupStateLegislators(request):
    addressSearch(request)


@require_http_methods(["POST"])
def renderResposne(request):
    if (
        "addressText" in request.POST.keys()
        and "lat" in request.POST.keys()
        and "lon" in request.POST.keys()
    ):
        address = request.POST["addressText"]
        if len(address) > 0:
            lat, lon = address2latlon(address)
        else:
            lat = request.POST["lat"]
            lon = request.POST["lon"]
    else:
        return JsonResponse({"status": "error"})

    logger.info(f"render body: {request.body}")
    location = getLocation(lat, lon)
    if not locationIsValid(location):
        return invalidState(request)
    results = getElectedOfficials(location)
    template = loader.get_template("contact.html")
    context = {
        "results": results,
    }
    context["title"] = "Render Response"
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET", "POST"])
def invalidState(request):
    template = loader.get_template("location-not-supported.html")
    context = {
        "title": "Invalid State",
    }
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def callSenatorCassidy(request):
    official = getSenatorCassidy()
    template = loader.get_template("redirect.html")
    context = getContext(request)
    context["target_url"] = f"tel:{official['office_phone']}"
    context["title"] = "Call Senator Cassidy"
    context["header"] = "Your United States Senator"
    context["results"] = [official]
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def callSenatorKennedy(request):
    official = getSenatorKennedy()
    template = loader.get_template("redirect.html")
    context = getContext(request)
    context["target_url"] = f"tel:{official['office_phone']}"
    context["title"] = "Call Senator Kennedy"
    context["header"] = "Your United States Senator"
    context["results"] = [official]
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def emailSenatorCassidy(request):
    official = getSenatorCassidy()
    target_url = f"{official['mailform']}"
    template = loader.get_template("redirect.html")
    context = getContext(request)
    context["target_url"] = target_url
    context["title"] = "Email Senator Cassidy"
    context["header"] = "Your United States Senator"
    context["results"] = [official]
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def emailSenatorKennedy(request):
    official = getSenatorKennedy()
    target_url = f"{official['mailform']}"
    template = loader.get_template("redirect.html")
    context = getContext(request)
    context["target_url"] = target_url
    context["title"] = "Email Senator Kennedy"
    context["header"] = "Your United States Senator"
    context["results"] = [official]
    return HttpResponse(template.render(context, request))
