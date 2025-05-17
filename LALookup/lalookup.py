import geopandas as gp
import csv
import logging
from shapely.geometry import Point
from django.conf import settings
from geopy.geocoders import Nominatim
from .models import Legislator, SoSElectedOfficial


logger = logging.getLogger(__name__)
GEO_TIMEOUT = 5


def latlon2Parish(lat, lon):
    geolocator = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.raw["address"]["county"]


def latlon2addr(lat, lon):
    geolocator = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    location = geolocator.reverse(f"{lat}, {lon}")
    return location.address


def address2latlon(address):
    # Nominatim Uses OpenStreet Map
    gc = Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT).geocode(address)
    return float(gc.latitude), float(gc.longitude)


def within_shape(df, shapes):
    in_shape = []
    for sh in shapes.geometry:
        within = df.within(sh)
        in_shape.append(within)
    return in_shape


def findShapeIndex(lat, lon, shape):
    for i in range(0, len(shape.geometry)):
        if shape.geometry[i].contains(Point(lon, lat)):
            return i


def getHouseDistrict(lat, lon):
    shape = gp.read_file(settings.HOUSEMAP)
    index = findShapeIndex(lat, lon, shape)
    if index:
        return int(shape.SLDLST[index])
    return -1


def getSenateDistrict(lat, lon):
    shape = gp.read_file(settings.SENATEMAP)
    index = findShapeIndex(lat, lon, shape)
    if index:
        return int(shape.SLDUST[index])
    return -1


def getStateRep(lat, lon):
    try:
        rep = Legislator.objects.get(
            districtnumber=getHouseDistrict(lat, lon), chamber="House"
        )
        return rep.todict()
    except Legislator.DoesNotExist as e:
        logger.error("ERROR: Rep not found {e}")
        return None


def getStateSenator(lat, lon):
    sen = Legislator.objects.filter(
        districtnumber=getSenateDistrict(lat, lon), chamber="Senate"
    ).first()
    if sen:
        return sen.todict()
    return None


def getStateLegislators(lat, lon):
    return [getStateSenator(lat, lon), getStateRep(lat, lon)]


def getMemberURL(chamber, member_id):
    if chamber == "House":
        return f"{settings.HOUSEMEMBERBASEURL}{member_id}"
    else:
        return f"{settings.SENATEMEMBERBASEURL}{member_id}"


def getMayor(lat, lon):
    try:
        location = (
            Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
            .reverse(f"{lat}, {lon}")
            .raw
        )
        city = location["address"]["city"]
        mayor = SoSElectedOfficial.objects.filter(
            officeTitle__icontains="Mayor", officeDescription__icontains=city
        ).first()
        return mayor.todict()
    except Legislator.DoesNotExist as e:
        logger.error("ERROR: Governor not found {e}")
        return None
    except AttributeError as e:
        logger.error("mayor not found")
        return None


def getGovernor(lat, lon):
    location = (
        Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
        .reverse(f"{lat}, {lon}")
        .raw
    )
    state = location["address"]["state"]
    gov = SoSElectedOfficial.objects.get(officeTitle="Governor")
    return gov.todict()


def getOfficials(lat, lon, officeTitle):
    official_list = []
    # location = (
    #     Nominatim(user_agent="LALookup", timeout=GEO_TIMEOUT)
    #     .reverse(f"{lat}, {lon}")
    #     .raw
    # )
    state = location["address"]["state"]
    officials = SoSElectedOfficial.object.filter(officeTitle=officeTitle).all()
    for off in officials:
        official_list.append(off.todict())
    return official_list


def getSenators(lat, lon):
    official_list = []
    # state = (
    #     Nominatim(user_agent="LALookup")
    #     .reverse(f"{lat}, {lon}")
    #     .raw["address"]["state"]
    # )
    officials = SoSElectedOfficial.objects.filter(officeTitle="U. S. Senator").all()
    for off in officials:
        official_list.append(off.todict())
    return official_list


def getElectedOfficials(lat, lon):
    elected_officials = []
    elected_officials.append(getStateSenator(lat, lon))
    elected_officials.append(getStateRep(lat, lon))
    elected_officials.append(getGovernor(lat, lon))
    elected_officials.append(getMayor(lat, lon))
    elected_officials += getSenators(lat, lon)
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
