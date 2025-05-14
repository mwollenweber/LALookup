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
from .lalookup import address2latlon, getStateLegislators, latlon2Parish, getStateRep


logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello, world. You're at the LALookup index.")


def redirect(request):
    template = loader.get_template("redirect.html")
    target_url = 'tel:504-952-6541'
    context = {"target_url": target_url}
    return HttpResponse(template.render(context, request))


@require_http_methods( ["POST"])
def addressSearch(request):
    try:
        if 'lat' in request.POST.keys() and 'lon' in request.POST.keys():
            lat = request.POST['lat']
            lon = request.POST['lon']
            address = ''
        elif 'address' in request.POST.keys():
            address = request.POST["address"]
            lat, lon = address2latlon(address)

        r = {
            "status": "success",
            "address": address,
            "lat": lat,
            "long": lon,
            "parish": latlon2Parish(lat, lon),
            "results": getStateLegislators(lat, lon),
        }
    except KeyError as e:
        r = {
            "status": "error",
            "message": f"KeyError: Missing {e}",
        }
    return JsonResponse(r)


@require_http_methods(["GET"])
def searchMe(request):
    template = loader.get_template("search.html")
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def locateMe(request):
    template = loader.get_template("locateme.html")
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def callMyRep(request):
    template = loader.get_template("search.html")
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def emailMyRep(request):
    print("emailMyRep")
    template = loader.get_template("locateme.html")

    #test data
    address = "4521 Magazine St, 70115"
    lat, lon = address2latlon(address)
    results = getStateRep(lat, lon)
    #results = getStateLegislators(lat, lon)
    context = {
        "results": results,
    }
    print("about to return")
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def callMySenator(request):
    template = loader.get_template("search.html")
    context = {}
    return HttpResponse(template.render(context, request))


@require_http_methods(["GET"])
def emailMySenator(request):
    template = loader.get_template("search.html")
    context = {}
    return HttpResponse(template.render(context, request))



def apitest(request):
    address = "4521 Magazine St, 70115"
    print("about to lat lon")
    lat, lon = address2latlon(address)
    print("lat lon")
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


