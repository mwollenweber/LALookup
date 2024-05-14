import traceback

import geopandas as gp
import csv
from shapely.geometry import Point
from pygris.geocode import geocode
from django.conf import settings
from geopy.geocoders import Nominatim
from .models import Legislator, SoSElectedOfficial


def latlon2Parish(lat, lon):
    try:
        geolocator = Nominatim(user_agent="LALookup")
        location = geolocator.reverse(f"{lat}, {lon}")
        return location.raw['address']['county']
    except Exception as e:
        traceback.print_exc()
        return None


def address2latlon(address):
    gc = geocode(address)
    return float(gc.latitude), float(gc.longitude)


def within_shape(df, shapes):
    in_shape = []
    for sh in shapes.geometry:
        within = df.within(sh)
        in_shape.append(within)
    return in_shape


def findShapeIndex(lat, lon, shape):
    for i in range(0, len(shape.geometry)):
        if (shape.geometry[i].contains(Point(lon, lat))):
            return i


def getHouseDistrict(lat, lon):
    shape = gp.read_file(settings.HOUSEMAP)
    index = findShapeIndex(lat, lon, shape)
    return int(shape.SLDLST[index])


def getSenateDistrict(lat, lon):
    shape = gp.read_file(settings.SENATEMAP)
    index = findShapeIndex(lat, lon, shape)
    return int(shape.SLDUST[index])


def getStateLegislators(lat, lon):
    try:
        rep = Legislator.objects.get(districtnumber=getHouseDistrict(lat, lon), chamber="House")
        sen = Legislator.objects.get(districtnumber=getSenateDistrict(lat, lon), chamber="Senate")
        return [rep.todict(), sen.todict()]
    except Legislator.DoesNotExist as e:
        print("ERROR: Legislator not found {e}")
        return None


def getMemberURL(chamber, member_id):
    if chamber == "House":
        return f"{settings.HOUSEMEMBERBASEURL}{member_id}"
    else:
        return f"{settings.SENATEMEMBERBASEURL}{member_id}"


def loadLegislators(filename, chamber):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            fullname = row['fullname']
            districtnumber = row['districtnumber']
            phone = row['districtofficephone']
            officeEmail = row['emailaddresspublic']

            print(f"{first_name} {last_name} {phone} {officeEmail}")
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


def splitName(fullname):
    try:
        parts = fullname.split()
        lastname = parts[-1]
        firstname = ' '.join(parts[:-1])
        return firstname, lastname
    except:
        return '', ''


def updateLegislatorParty():
    for L in Legislator.objects.all():
        try:
            # todo #fixme this isn't a great search
            # todo #fixme there can be more than one office title
            sos = (SoSElectedOfficial.objects.filter(
                first_name=L.first_name,
                last_name=L.last_name)
                   .exclude(officeTitle='DSCC Member')
                   .exclude(officeTitle='RSCC Member')
                   .first())

            print(f"{L.first_name} {L.last_name} {sos.party}")
            L.party = sos.party
            L.gender = sos.gender
            # L.parish = sos.parish
            L.officeTitle = sos.officeTitle
            L.save()
        except Exception as e:
            print(f"ERROR: {e}")


def loadElectedOfficials(filename):
    print(f"loading {filename}")
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(dict(row))
            officeTitle = row['Office Title'].strip()
            officeDescription = row['Office Description']
            candidateName = row['Candidate Name']
            first_name, last_name = splitName(candidateName)
            officePhone = row['Office Phone']
            phone = row['Phone']
            ethnicity = row['Ethnicity']
            gender = row['Sex']
            party = row['Party Code']
            office_level = row['Office Level']
            # exp_date = row['Expiration Date']
            comm_date = row['Commissioned Date']
            parish = row['Parish']
            email = row['Email']
            print(f"{officeTitle} {first_name} {last_name} {phone} {email} {party} {gender}")
            obj, created = SoSElectedOfficial.objects.update_or_create(
                officeTitle=officeTitle,
                first_name=first_name,
                last_name=last_name,
                party=party,
                gender=gender,
                ethnicity=ethnicity,
                email=email,
                officeDescription=officeDescription,
                officeLevel=office_level,
                # expirationDate=exp_date,
                parish=parish,
                officePhone=officePhone,
                phone=phone,
            )
