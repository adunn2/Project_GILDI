import urllib.request
import json
import requests

#headers = {'x-api-key':'your_key'}
#payload = {
#    'lat':34.071783,
#    'lng':-118.2596,
#    'searchtype':'addresscoord',
#    'getloma':'False'
#    }
#s = requests.get('https://api.nationalflooddata.com/data',headers=headers,params=payload)

def getWeatherAlerts():
    nwsEndpoint ="https://api.weather.gov/alerts"
    return requests.get(nwsEndpoint)



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
