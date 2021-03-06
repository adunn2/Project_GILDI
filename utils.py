import urllib.request
import json
import requests


# This loads a json file with credentials for services
def loadCreds(fileName = "api_credentials.json"):
    try:
        with open(fileName) as apiFile:
            return json.load(apiFile)
    except Exception as e:
        print("File load error\n", e)


# This makes a simple request to the data parsing code.
def runDataApp(state):
    payload = {'state': state}
    dataEndpoint ="http://projectgildi_flaskdataapp_1:5091"
    res = requests.get(dataEndpoint, params=payload)
    return res

# This makes a simple request to get event coordinates.
def runGetEventLocations(state):
    payload = {'state': state.upper()}
    dataEndpoint ="http://projectgildi_flaskdataapp_1:5091/events"
    res = requests.get(dataEndpoint, params=payload)
    return res


# This makes a simple request to the National weather service to get the first 10 active weather alerts.
def getWeatherAlerts():
    nwsEndpoint ="https://api.weather.gov/alerts/active?limit=10"
    res = requests.get(nwsEndpoint)
    return res

# This makes a simple request to the National weather service to get the first 10 active weather alerts.
def getLocalWeatherAlerts():
    nwsEndpoint ="https://api.weather.gov/alerts/active/area/MD"
    res = requests.get(nwsEndpoint)
    return res


# def getWeatherAlerts():
#     nwsEndpoint ="https://api.weather.gov/alerts/active?limit=10"
#     res = requests.get(nwsEndpoint)
#     return res





#headers = {'x-api-key':'your_key'}
#payload = {
#    'lat':34.071783,
#    'lng':-118.2596,
#    'searchtype':'addresscoord',
#    'getloma':'False'
#    }
#s = requests.get('https://api.nationalflooddata.com/data',headers=headers,params=payload)


# endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
#
#
# api_key = ""

#origin = input('Your location?').replace(' ', '+')
#destination = input('Destination').replace(' ', '+')
#basic = "origin=Disneyland&destination=Universal+Studios+Hollywood&key=YOUR_API_KEY"
#nav_request = "origin={}&destination={}&key={}".format(origin,destination,api_key)

#request = endpoint + nav_request

#request2 = "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key="

#print(request)

#response = urllib.request.urlopen(request+api_key).read()

#directions = json.loads(response)

#print(directions)
#request = "https://maps.googleapis.com/maps/api/directions/json?origin=odenton&destination=laurel&key="
# request = "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key="
#
# response = urllib.request.urlopen(request+api_key).read()
#
# directions = json.loads(response)
#
# print(directions)
