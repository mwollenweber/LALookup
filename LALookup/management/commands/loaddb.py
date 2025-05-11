import logging
from LALookup.lalookup import (
    loadLegislators,
    loadElectedOfficials,
    updateLegislatorParty,
)
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, **options):
        print("loaddb")
        filename = "./data/HouseMembers.csv"
        loadLegislators(filename, "House")

        filename = "./data/SenateMembers.csv"
        loadLegislators(filename, "Senate")

        filename = "./data/ElectedOfficials.csv"
        loadElectedOfficials(filename)

        updateLegislatorParty()
        print("done")
