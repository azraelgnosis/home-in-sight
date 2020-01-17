from flask import current_app, g


zws_id = 'X1-ZWz17gbocdcidn_90hcq'

def get_properties():
    if 'properties' not in g:
        path = current_app.config['PROPERTIES']

        with open(path, 'r') as f:
            properties = json.load(f)
            g.properties = properties

    return g.properties

def get_property(zpid:int):
    if 'properties' not in g:
        get_properties()
    
    return g.properties[zpid]
