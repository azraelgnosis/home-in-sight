import sqlite3
import click
import json
from flask import current_app, g
from flask.cli import with_appcontext
import os

config_path = os.path.join(os.getcwd(), "instance", "config.json") #current_app.config['CONFIG']
with open(config_path, "r") as f:
    config_data = json.load(f)
    
zws_id = config_data["zws_id"] # 'X1-ZWz17gbocdcidn_90hcq'
google_api_key = config_data['google_api_key']

STATES = ("GA",)

POI_types = ("Library", "Cafe")


def get_properties():
    if 'properties' not in g:
        path = current_app.config['DATA']

        with open(path, 'r') as f:
            properties = json.load(f)
            g.properties = properties

    return g.properties

def get_property(zpid:int):
    if 'properties' not in g:
        get_properties()
    
    return g.properties[zpid]









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