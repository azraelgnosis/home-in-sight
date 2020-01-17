from flask import (
    Blueprint, render_template, request, session
)

import requests

from xml.etree.ElementTree as ET

from .data import zws_id, get_properties

bp = Blueprint('insight', __name__, url_prefix="/")

@bp.route('/', methods=('GET', 'POST'))
def test():
    if session.method == 'POST':
        get_updated_property_details = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"
        zp_id = session.form['zpid']

        url = f"{get_updated_property_details}?zws-id={zws_id}&zpid={zp_id}"

        #http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=<ZWSID>&zpid=48749425

    data = requests.get(url)
    print(data.content)
    r = request()

    return render_template("index.html")

@bp.route('/properties', methods=('GET'))
def properties():
    properties = get_properties()

    return render_template("properties.html", properties=properties)