import sqlite3
import click
import json
from flask import current_app, g
from flask.cli import with_appcontext
import os

data_path = os.path.join(os.getcwd(), "home_in_sight", "data")
config_path = os.path.join(os.getcwd(), "instance", "config.json") #current_app.config['CONFIG']
with open(config_path, "r") as f:
    config_data = json.load(f)
    
zws_id = config_data["zws_id"] # 'X1-ZWz17gbocdcidn_90hcq'
google_api_key = config_data['google_api_key']

STATES = ("GA",)

POI_types = ("Restaurant", "Grocer", "Library", "Cafe", "Park", "Airport", "Lake", "River", "Hospital", "University", "Theater")

def get_FIPS_codes():
    FIPS_path = os.path.join(data_path, "FIPS_codes.json")

    with open(FIPS_path, "r") as f: 
        FIPS_codes = json.load(f)
    
    return FIPS_codes

def get_county(fips_code:str) -> str:
    FIPS_codes = get_FIPS_codes()
    state = FIPS_codes.get(fips_code[:2])
    county = state.get(fips_code[2:])

    return county

def get_properties():
    '''
    Checks g to see if properties has already been loaded into memory.
    If not, properties.json is loaded and added to g, then returned.
    '''
    if 'properties' not in g:
        properties_path = os.path.join(data_path, "properties.json") # os.path.join(current_app.config['DATA'], "properties.json")

        with open(properties_path, 'r') as f:
            properties = json.load(f)
            g.properties = properties

    return g.properties

def get_property(street:str, city:str, state:str):
    '''
    Calls get_properties(), 
    then returns the property matching the provided Zillow id
    '''
    properties = get_properties()
    state_counties = properties.get(state)

    try:
        for county, county_properties in state_counties.items():
            for Property in county_properties:
                if f"{street}, {city}, {state}" == list(Property)[0]:
                    return Property
    except TypeError:
        return None
    
    return None

def record_property(Property:"Property"):
    '''
    Loads properties, then adds provided property to the
    dict
    '''
    properties = get_properties()

    state = Property.state
    county = Property.county

    if not properties.get(state):
        properties[state] = {}
    state_properties = properties.get(state)

    if not state_properties.get(county):
        state_properties[county] = []
    county_properties = state_properties.get(Property.county)

    if Property.json() not in county_properties:
        county_properties.append(Property.json())

def record_properties(new_properties:list):
    '''
    Loads properties.json, iterates through new_properties
    then writes properties to properties.json
    '''
    properties = get_properties()

    for Property in new_properties:
        record_property(Property)

    properties_path = os.path.join(data_path, "properties.json")
    with open(properties_path, "w") as f:
        json.dump(properties, f)












def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.confid['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create new tables."""
    init_db()
    click.echo('Initialized the database.')