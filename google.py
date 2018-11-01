import googlemaps
from datetime import datetime

############################################################
# Full documentation can be found where
# https://github.com/googlemaps/google-maps-services-python
############################################################

# Gets the elevation at a lat lng point
def getElevation(google_api_key):
    gmaps = googlemaps.Client(key=google_api_key)
    # Geocoding an address
    google_result = gmaps.elevation((39.7391536,-104.9847034))
    return google_result


def getGeoCode(google_api_key):
    gmaps = googlemaps.Client(key=google_api_key)
    # Geocoding an address
    google_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    return google_result
