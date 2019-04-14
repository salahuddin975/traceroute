import geocoder
from geopy.geocoders import Nominatim


def print_geolocation(route_info):

    for hop_addr in route_info:
        addr = hop_addr[1]
        g = geocoder.ip(addr)

        try:
            geolocator = Nominatim(user_agent="specify_your_app_name_here")
            geo_addr = str(g.latlng[0]) + ', ' + str(g.latlng[1])

            location = geolocator.reverse(geo_addr)
            print addr, "-", location, " (" + str(g.latlng[0]) + ", " + str(g.latlng[1]) + ")"
        except:
            print addr, "not solved!"

