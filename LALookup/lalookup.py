import geopandas as gp
import csv
import logging
import googlemaps
from shapely.geometry import Point
from django.conf import settings
from .models import Legislator, SoSElectedOfficial, Campaign
from .settings import SUPPORTED_STATES, GMAP_APIKEY

logger = logging.getLogger(__name__)


def getActiveCampaigns():
    return Campaign.objects.filter(enabled=True, is_public=True).all()


def getContext(request):
    context = {}
    context["title"] = "Louisiana Progressive Action: Be Heard!"
    context["header"] = "Contact Your Elected Official"
    context["description"] = (
        "Be Heard! Contact Your Elected Official with Louisiana Progressive Action"
    )
    context["url"] = request.build_absolute_uri()

    if "campaignID" in request.GET:
        campaign = Campaign.objects.filter(id=request.GET["campaignID"]).first()
        if campaign:
            context["campaign_id"] = campaign.id
            context["title"] = campaign.title
            context["header"] = campaign.header
            context["campaign_prompt"] = campaign.prompt.splitlines()
            context["description"] = campaign.description
            context["image_url"] = campaign.image_url
            campaign.hit_count += 1
            campaign.save()
    return context


def locationIsValid(location):
    try:
        print("42")
        print(location)
        state = location["state"]
        state = location["state"]
        return state in SUPPORTED_STATES
    except AttributeError:
        return False


def getCityName(address_components):
    for component in address_components:
        if "locality" in component["types"]:
            return component["long_name"]


def getStateName(address_components):
    for component in address_components:
        if "administrative_area_level_1" in component["types"]:
            return component["long_name"]


def getCountyName(address_components):
    for component in address_components:
        if "administrative_area_level_2" in component["types"]:
            return component["long_name"]


def getLocation(lat, lon):
    gmaps = googlemaps.Client(key=GMAP_APIKEY)
    geocode_result = gmaps.reverse_geocode((lat, lon))[0]
    geocode_result["state"] = getStateName(geocode_result["address_components"])
    geocode_result["city"] = getCityName(geocode_result["address_components"])
    geocode_result["county"] = getCountyName(geocode_result["address_components"])
    geocode_result["address"] = geocode_result["formatted_address"]
    geocode_result["lat"] = geocode_result["geometry"]["location"]["lat"]
    geocode_result["lon"] = geocode_result["geometry"]["location"]["lng"]
    return geocode_result


def latlon2addr(lat, lon):
    gmaps = googlemaps.Client(key=GMAP_APIKEY)
    geocode_result = gmaps.reverse_geocode((lat, lon))[0]
    return geocode_result["formatted_address"]


def address2latlon(address):
    try:
        gmaps = googlemaps.Client(key=GMAP_APIKEY)
        geocode_result = gmaps.geocode(address)[0]
        return (
            geocode_result["geometry"]["location"]["lat"],
            geocode_result["geometry"]["location"]["lng"],
        )
    except AttributeError as e:
        logger.error("Address could not be geocoded")
        return 0.0, 0.0


def findShapeIndex(lat, lon, shape):
    for i in range(0, len(shape.geometry)):
        if shape.geometry[i].contains(Point(lon, lat)):
            return i


def getCongressIndex(lat, lon):
    shape = gp.read_file(settings.CONGRESSMAP)
    shape = shape.to_crs("EPSG:4269")
    index = findShapeIndex(lat, lon, shape)
    return index


def getCongressDistrict(lat, lon):
    shape = gp.read_file(settings.CONGRESSMAP)
    shape = shape.to_crs("EPSG:4269")
    index = findShapeIndex(lat, lon, shape)
    return shape.OFFICE_ID[index]


def getUSRep(location):
    shape = gp.read_file(settings.CONGRESSMAP)
    shape = shape.to_crs("EPSG:4269")
    index = findShapeIndex(location["lat"], location["lon"], shape)
    rep = SoSElectedOfficial.objects.filter(
        officeTitle__icontains="U. S. Representative",
        first_name__icontains=shape.FIRSTNAME[index],
        last_name__icontains=shape.LASTNAME[index],
    ).first()
    return rep.todict() if rep else None


def getHouseDistrict(lat, lon):
    shape = gp.read_file(settings.HOUSEMAP)
    index = findShapeIndex(lat, lon, shape)
    return int(shape.SLDLST[index]) if index else -1


def getSenateDistrict(lat, lon):
    shape = gp.read_file(settings.SENATEMAP)
    index = findShapeIndex(lat, lon, shape)
    return int(shape.SLDUST[index]) if index else -1


def getStateRep(location):
    rep = Legislator.objects.get(
        districtnumber=getHouseDistrict(location["lat"], location["lon"]),
        chamber="House",
    )
    return rep.todict() if rep else None


def getStateSenator(location):
    sen = Legislator.objects.filter(
        districtnumber=getSenateDistrict(location["lat"], location["lon"]),
        chamber="Senate",
    ).first()
    return sen.todict() if sen else None


def getStateLegislators(location):
    return [getStateSenator(location), getStateRep(location)]


def getMemberURL(chamber, member_id):
    if chamber == "House":
        return f"{settings.HOUSEMEMBERBASEURL}{member_id}"
    else:
        return f"{settings.SENATEMEMBERBASEURL}{member_id}"


def getMayor(location):
    try:
        city = location["city"]
        mayor = SoSElectedOfficial.objects.filter(
            officeTitle__icontains="Mayor", officeDescription__icontains=city
        ).first()
        return mayor.todict()
    except AttributeError as e:
        logger.error("mayor not found")
        return None


def getGovernor(location):
    state = location["state"]
    gov = SoSElectedOfficial.objects.get(officeTitle="Governor")
    return gov.todict() if gov else None


def getSenators(location):
    official_list = []
    officials = SoSElectedOfficial.objects.filter(officeTitle="U. S. Senator").all()
    for off in officials:
        official_list.append(off.todict())
    return official_list


def getSenatorByName(last_name):
    official = SoSElectedOfficial.objects.filter(
        officeTitle="U. S. Senator", last_name__icontains=last_name
    ).first()
    return official.todict() if official else None


def getSenatorCassidy():
    return getSenatorByName("Cassidy")


def getSenatorKennedy():
    return getSenatorByName("Kennedy")


def getElectedOfficials(location):
    elected_officials = []
    elected_officials.append(getStateSenator(location))
    elected_officials.append(getStateRep(location))
    elected_officials.append(getGovernor(location))
    elected_officials.append(getMayor(location))
    elected_officials.append(getUSRep(location))
    elected_officials += getSenators(location)
    return elected_officials


def loadLegislators(filename, chamber):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row["first_name"]
            last_name = row["last_name"]
            fullname = row["fullname"]
            districtnumber = row["districtnumber"]
            phone = row["districtofficephone"]
            officeEmail = row["emailaddresspublic"]

            logger.debug(f"{first_name} {last_name} {phone} {officeEmail}")
            obj, created = Legislator.objects.update_or_create(
                first_name=first_name,
                last_name=last_name,
                fullname=fullname,
                districtnumber=districtnumber,
                officePhone=phone,
                officeEmail=officeEmail,
                officeURL=getMemberURL(chamber, districtnumber),
                chamber=chamber,
            )


# fixme: wtf is this?
def splitName(fullname):
    try:
        parts = fullname.split()
        lastname = parts[-1]
        firstname = " ".join(parts[:-1])
        return firstname, lastname
    except:
        return "", ""


def updateLegislatorParty():
    for L in Legislator.objects.all():
        try:
            # todo #fixme this isn't a great search
            # todo #fixme there can be more than one office title
            sos = (
                SoSElectedOfficial.objects.filter(
                    first_name=L.first_name, last_name=L.last_name
                )
                .exclude(officeTitle="DSCC Member")
                .exclude(officeTitle="RSCC Member")
                .first()
            )

            logger.debug(f"{L.first_name} {L.last_name} {sos.party}")
            L.party = sos.party
            L.gender = sos.gender
            # L.parish = sos.parish
            L.officeTitle = sos.officeTitle
            L.save()
        except Exception as e:
            logger.error(f"ERROR: {e}")


def loadElectedOfficials(filename):
    logger.info(f"loading {filename}")
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logger.debug(dict(row))
            officeTitle = row["Office Title"].strip()
            officeDescription = row["Office Description"]
            candidateName = row["Candidate Name"]
            first_name, last_name = splitName(candidateName)
            officePhone = row["Office Phone"]
            phone = row["Phone"]
            ethnicity = row["Ethnicity"]
            gender = row["Sex"]
            party = row["Party Code"]
            office_level = row["Office Level"]
            # exp_date = row['Expiration Date']
            comm_date = row["Commissioned Date"]
            parish = row["Parish"]
            email = row["Email"]
            logger.debug(
                f"{officeTitle} {first_name} {last_name} {phone} {email} {party} {gender}"
            )
            obj, created = SoSElectedOfficial.objects.update_or_create(
                officeTitle=officeTitle,
                first_name=first_name,
                last_name=last_name,
                party=party,
                gender=gender,
                ethnicity=ethnicity,
                # personalEmail=email,
                officeDescription=officeDescription,
                officeLevel=office_level,
                # expirationDate=exp_date,
                parish=parish,
                officePhone=officePhone,
                personalPhone=phone,
            )
