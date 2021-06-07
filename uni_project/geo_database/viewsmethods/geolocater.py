import geopy
from geopy.geocoders import Nominatim

def reverse_locate(lat, long):
    #using openstreetmapquest
    geolocator = Nominatim(user_agent="geo_database")
    locationList = [lat, long]
    coordinates = ", ".join(map(str, locationList))
    print(type(coordinates))
    # coordinates = "52.509669, 13.376294"
    location = geolocator.reverse(coordinates)
    print(location.address)