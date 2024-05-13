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
from .lalookup import address2latlon, getStateLegislators


def index(request):
    return HttpResponse("Hello, world. You're at the LALookup index.")


@require_http_methods(["GET", "POST"])
def addressSearch(request):
    if request.method == 'GET':
        template = loader.get_template('search.html')
        context = {}
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        print('Raw Data: "%s"' % request.body)
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                address = data['address']
                if len(address) > 5:
                    lat, lon = address2latlon(address)
                else:
                    lat = data['lat']
                    lon = data['lon']

                r = {
                    'address': address,
                    'lat': lat,
                    'long': lon,
                    'parish': '',
                    'state_legislators': getStateLegislators(lat, lon)
                }
                return JsonResponse(r)

            except json.JSONDecodeError as e:
                traceback.print_exc()
                return JsonResponse({'error': 'Invalid JSON'})

            except KeyError as e:
                traceback.print_exc()
                return JsonResponse({'error': 'An error occurred'})

            except Exception as e:
                traceback.print_exc()
                return JsonResponse({'error': 'An error occurred'})
        else: #not json
            try:
                address = request.POST['address']
                if len(address) > 5:
                    lat, lon = address2latlon(address)
                else:
                    lat = request.POST['lat']
                    lon = request.POST['lon']

                r = {
                    'address': address,
                    'lat': lat,
                    'long': lon,
                    'parish': '',
                    'state_legislators': getStateLegislators(lat, lon)
                }
                #fixme -- shouldn't return json
                #should be some type of formatted response
                #https://getbootstrap.com/docs/4.3/components/card/
                return HttpResponse(str(r))

            except Exception as e:
                traceback.print_exc()
                return HttpResponse("An error occurred")


def test(request):
    query = "4521 Magazine St, 70115"
    lat, lon = address2latlon(query)
    r = {
        'query': query,
        'lat': lat,
        'long': lon,
        'parish': '',
        'state_legislators': getStateLegislators(lat, lon)
    }
    return JsonResponse(r)


def LookupStateLegislators(request):
    search(request)


def contact(request):
    template = loader.get_template('contact.html')
    context = {}
    return HttpResponse(template.render(context, request))

