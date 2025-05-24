import geopandas as gp
import csv
import logging
from shapely.geometry import Point
from django.conf import settings
from geopy.geocoders import Nominatim
from .models import Legislator, SoSElectedOfficial
from .settings import SUPPORTED_STATES, GEO_TIMEOUT

logger = logging.getLogger(__name__)


def locationIsValid(location):
    if "address" in location.raw:
        state = location.raw["address"]["state"]
        return state in SUPPORTED_STATES
    return False


def getLocation(lat, lon):
    geolocator = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location


def latlon2Parish(lat, lon):
    geolocator = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.raw["address"]["county"]


def latlon2addr(lat, lon):
    geolocator = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.address


def address2latlon(address):
    gc = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT).geocode(address)
    return float(gc.latitude), float(gc.longitude)


def address2location(address):
    return Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT).geocode(address)


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
    index = findShapeIndex(location.latitude, location.longitude, shape)
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
        districtnumber=getHouseDistrict(location.latitude, location.longitude),
        chamber="House",
    )
    return rep.todict() if rep else None


def getStateSenator(location):
    sen = Legislator.objects.filter(
        districtnumber=getSenateDistrict(location.latitude, location.longitude),
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
        city = location.raw["address"]["city"]
        mayor = SoSElectedOfficial.objects.filter(
            officeTitle__icontains="Mayor", officeDescription__icontains=city
        ).first()
        return mayor.todict()
    except AttributeError as e:
        logger.error("mayor not found")
        return None


def getGovernor(location):
    state = location.raw["address"]["state"]
    gov = SoSElectedOfficial.objects.get(officeTitle="Governor")
    return gov.todict() if gov else None


def getOfficials(location, officeTitle):
    official_list = []
    # location = (
    #     Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    #     .reverse(f"{lat}, {lon}")
    #     .raw
    # )
    # state = location["address"]["state"]
    officials = SoSElectedOfficial.object.filter(officeTitle=officeTitle).all()
    for off in officials:
        official_list.append(off.todict())
    return official_list


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
