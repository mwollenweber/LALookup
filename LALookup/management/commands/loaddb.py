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
        logger.info("Loading DB")
        logger.info("Loading House")
        filename = "./data/HouseMembers.csv"
        loadLegislators(filename, "House")
        logger.info("Done loading House Members")

        logger.info("Loading Senate")
        filename = "./data/SenateMembers.csv"
        loadLegislators(filename, "Senate")
        logger.info("Done loading Senate Members")

        logger.info("Loading Elected Officials")
        filename = "./data/ElectedOfficials.csv"
        loadElectedOfficials(filename)
        logger.info("Done loading Elected Officials")

        logger.info("Loading Party")
        updateLegislatorParty()
        logger.info("Done")
