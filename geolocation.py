import geocoder
from geopy.geocoders import Nominatim

import pycurl
from StringIO import StringIO


def get_organization_name(ip_addr):
    url = 'https://ipinfo.io/' + ip_addr

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()

    body_org = body[body.find("Organization</span>"):]
    body_org = body_org[body_org.find("<span>"):]
    org_name = body_org[body_org.find("<span>") + 6: body_org.find("</span>")]

    return org_name


def print_geolocation(route_info):

    for hop_addr in route_info:
        addr = hop_addr[1]

        if addr == "":
            print hop_addr[0], "  *   *   *"
            continue

        org_name = get_organization_name(addr)

        g = geocoder.ip(addr)

        try:
            geolocator = Nominatim(user_agent="specify_your_app_name_here")
            geo_addr = str(g.latlng[0]) + ', ' + str(g.latlng[1])

            location = geolocator.reverse(geo_addr)
            print hop_addr[0],"  IP: " + str(addr) + ",  Org: " + str(org_name) + ",  Location: " + str(location) +\
                             " (" + str(g.latlng[0]) + ", " + str(g.latlng[1]) + ")"
        except:
            print hop_addr[0]," ",addr, "not resolved!"

