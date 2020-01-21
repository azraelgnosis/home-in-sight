from flask import (
    Blueprint, render_template, request,
)

import requests
import xml.etree.ElementTree as ET

from .data import zws_id, get_properties, STATES
from .models import Property

bp = Blueprint('insight', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']

        url = deep_search_url(zws_id, street, city, state)
        print(url)
        response = requests.get(url)
        root = ET.fromstring(response.content)
        new_property = create_property(root)

        return render_template("index.html", states=STATES, Property=new_property.json())

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
    use_code = result.find("useCode").text
    year_built = int(result.find("yearBuilt").text)
    lot_area = int(result.find("lotSizeSqFt").text)
    property_area = int(result.find("finishedSqFt").text)
    baths = float(result.find("bathrooms").text)
    beds = int(result.find("bedrooms").text)

    new_property =  Property(street, city, state, zipcode,
        longitude = longitude,
        latitude = latitude,
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


def get_POIs(property:Property):
    from .data import POIs
    pass