import geocoder

g = geocoder.ip("68.85.247.229")

print g.latlng


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")

addr = str(g.latlng[0]) + ', ' + str(g.latlng[1])
location = geolocator.reverse(addr)
print(location.address)

