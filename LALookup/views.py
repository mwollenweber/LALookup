import logging
import traceback
import json
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.html import escape
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.conf import settings
from .lalookup import (
    address2latlon,
    getStateLegislators,
    latlon2Parish,
    getStateRep,
    getStateSenator,
)

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello, world. You're at the LALookup index.")


@require_http_methods(["POST", "GET"])
def addressSearch(request):
    if "lat" in request.POST.keys() and "lon" in request.POST.keys():
        lat = request.POST["lat"]
        lon = request.POST["lon"]
        address = ""
    elif "address" in request.POST.keys():
        address = request.POST["address"]
        lat, lon = address2latlon(address)
    elif "lat" in request.GET.keys() and "lon" in request.GET.keys():
        lat = request.GET["lat"]
        lon = request.GET["lon"]
        address = ""
    elif "address" in request.GET.keys():
        address = request.GET["address"]
        lat, lon = address2latlon(address)
    else:
        return JsonResponse({
            "status": "error",
            "message": f"You must provide an address or lat+lon",
        })
    r = {
        "status": "success",
        "address": address,
        "lat": lat,
        "long": lon,
        "parish": latlon2Parish(lat, lon),
        "results": getStateLegislators(lat, lon),
    }
    return JsonResponse(r)


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
        official = getStateRep(lat, lon)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = {
            "target_url": target_url,
            "header": "Your State Representative",
            "results": [official],
        }
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
        official = getStateRep(lat, lon)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = {
            "target_url": target_url,
            "header": "Your State Representative",
            "results": [official],
        }
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
        official = getStateSenator(lat, lon)
        target_url = f"tel:{official['office_phone']}"
        template = loader.get_template("redirect.html")
        context = {
            "target_url": target_url,
            "header": "Your State Senator",
            "results": [official],
        }
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
        official = getStateSenator(lat, lon)
        target_url = f"mailto:{official['email']}"
        template = loader.get_template("redirect.html")
        context = {
            "target_url": target_url,
            "header": "Your State Senator",
            "results": [official],
        }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("locateme.html")
        context = {}
        return HttpResponse(template.render(context, request))


def apitest(request):
    address = "4521 Magazine St, 70115"
    lat, lon = address2latlon(address)
    r = {
        "status": "success",
        "address": address,
        "lat": lat,
        "long": lon,
        "parish": latlon2Parish(lat, lon),
        "results": getStateLegislators(lat, lon),
    }
    return JsonResponse(r)


def test(request):
    address = "4521 Magazine St, 70115"
    lat, lon = address2latlon(address)
    results = getStateLegislators(lat, lon)
    logger.info(f"render body: {request.body}")
    template = loader.get_template("contact.html")
    context = {
        "results": results,
    }
    return HttpResponse(template.render(context, request))


def LookupStateLegislators(request):
    addressSearch(request)


def renderResposne(request, response=None):
    lat = request.POST["lat"]
    lon = request.POST["lon"]
    results = getStateLegislators(lat, lon)

    logger.info(f"render body: {request.body}")
    template = loader.get_template("contact.html")
    context = {
        "results": results,
    }
    return HttpResponse(template.render(context, request))
