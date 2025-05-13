from django.conf import settings
from .lalookup import loadLegislators
from .celery import app


@app.task(name="test")
def test():
    print("This is a test")


@app.task(name="loadLegislators")
def runLoadLegislatorss():
    loadLegislators(settings.HOUSEMEMBERS, "House")
    loadLegislators(settings.SENATEMEMBERS, "Senate")
