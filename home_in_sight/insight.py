from flask import (
    Blueprint, render_template, request,
)

import requests
import xml.etree.ElementTree as ET

from .data import zws_id, google_api_key, get_properties, get_property, STATES, record_properties
from .models import Property, POI

bp = Blueprint('insight', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']

        new_property = get_property(street, city, state)
            
        if not new_property:
            url = deep_search_url(zws_id, street, city, state)
            print(url)
            response = requests.get(url)
            root = ET.fromstring(response.content)
            new_property = create_property(root)

        get_POIs(new_property)
        record_properties([new_property])

        return render_template("index.html", states=STATES, Property=new_property)

    return render_template("index.html", states=STATES)

def url_string(string:str):
    return string.replace(" ", "+")

def deep_search_url(zws_id, street, city, state):
    deep_search = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
    street = url_string(street)

    deep_search_url = f"{deep_search}?zws-id={zws_id}&address={street}&citystatezip={city}+{state}"
    return deep_search_url

def create_property(root:ET.Element):
    property_data = {} # TODO convert to dict

    request = root.find("request")
    street = request.find("address").text
    citystate = request.find("citystatezip").text.split(" ")
    city = " ".join(citystate[0:-1])
    state = "".join(citystate[-1:])
    response = root.find("response")
    result = response.find("results").find("result")
    zpid = int(result.find("zpid").text)
    links = result.find("links")
    url = links.find("homedetails").text
    address = result.find("address")
    zipcode = int(address.find("zipcode").text)
    latitude = float(address.find("latitude").text)
    longitude = float(address.find("longitude").text)
    FIPS_code = result.find("FIPScounty").text
    use_code = result.find("useCode").text
    year_built = int(result.find("yearBuilt").text)
    lot_area = int(result.find("lotSizeSqFt").text)
    property_area = int(result.find("finishedSqFt").text)
    baths = float(result.find("bathrooms").text)
    beds = int(result.find("bedrooms").text)

    new_property = Property(street, city, state, zipcode,
        longitude = longitude,
        latitude = latitude,
        FIPS_code = FIPS_code,
        zpid = zpid,
        url = url,
        use_code = use_code,
        beds = beds,
        baths = baths,
        property_area = property_area,
        lot_area = lot_area,
        year_built = year_built,
    )

    return new_property


def get_POIs(Property:Property):
    lng = Property.longitude
    lat = Property.latitude

    from .data import POI_types
    find_place = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery"
    radius = 16000 # radius in km
    locationbias = f"&locationbias=circle:{radius}@{lat},{lng}"
    fields = "&fields=" + ",".join(["formatted_address", "name", "geometry/location/lat", "geometry/location/lng", "place_id"])
    find_place_url = f"{find_place}{fields}{locationbias}&key={google_api_key}"
    
    for Type in POI_types:
        url = find_place_url + f"&input={Type}"
        print(url)
        response = requests.get(url)
        print(response.json())
        point = POI.from_json(response.json())
        point.distance = POI.calc_distance(Property, point)
        Property.add_POI(Type, point)
