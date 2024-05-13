from LALookup.lalookup import loadLegislators, loadElectedOfficials, updateLegislatorParty


filename = './data/HouseMembers.csv'
loadLegislators(filename, "House")

filename = './data/SenateMembers.csv'
loadLegislators(filename, "Senate")

filename = './data/ElectedOfficials.csv'
loadElectedOfficials(filename)

updateLegislatorParty()

