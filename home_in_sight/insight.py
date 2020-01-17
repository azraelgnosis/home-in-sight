from flask import (
    Blueprint, render_template, request,
)

import requests
import xml.etree.ElementTree as ET

from .data import zws_id, get_properties, STATES

bp = Blueprint('insight', __name__)



@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']

        print(street, city, state)
        url = deep_search_url(zws_id, street, city, state)
        response = requests.get(url)
        print(response.content)

    return render_template("index.html", states=STATES)

# @bp.route('/properties', methods=('GET'))
# def properties():
#     properties = get_properties()

#     return render_template("properties.html", properties=properties)

def url_string(string:str):
    return string.replace(" ", "+")

def deep_search_url(zws_id, street, city, state):
    deep_search = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
    street = url_string(street)

    deep_search_url = f"{deep_search}?zws-id={zws_id}&address={street}&statezip={city}+{state}"
    return deep_search_url