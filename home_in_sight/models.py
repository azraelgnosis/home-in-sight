class Location:
    __slots__ = ["id", "location", "address", "street", "city", "state", "zipcode", "longitude", "latitude", "type"]

    def __init__(self):
        self.id = None
        self.address = None
        self.street = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.longitude = None
        self.latitude = None

    def _set_location(self):
        self.location = f"{self.address} {self.city}, {self.state} {self.zipcode}"

    def json(self):
        json = {
            "location": {
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "zip code": self.zipcode,
                "address": f"{self.street}, {self.city}, {self.state} {self.zipcode}"
            },
            "coordinates": {
                "longitude": self.longitude,
                "latitude": self.latitude
            },
            # etc.

        }

        return json

class Property(Location):
    __slots__ = ["id", "zpid", "location", "address", "street", "city", "state", "zipcode", "longitude", "latitude", "url", "images", "use_code", "beds", "baths", "property_area", "lot_area", "year_built", "year_updated"]
    def __init__(self):
        self.zpid = None
        self.url = None
        self.location = None
        self.address = None
        self.street = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.longitude = None
        self.latitude = None
        self.url = None
        self.images = []
        self.use_code = None
        self.beds = None
        self.baths = None
        self.property_area = None
        self.lot_area = None
        self.year_built = None
        self.year_updated = None

    def json(self):
        json = {
            "zpid": self.zpid,
            "url": self.url,
            "location": {
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "zip code": self.zipcode,
                "address": f"{self.street}, {self.city}, {self.state} {self.zipcode}"
            },
            "coordinates": {
                "longitude": self.longitude,
                "latitude": self.latitude
            },
            "images": [link for link in self.images],
            # etc.

        }

        return json

class POI(Location):
    __slots__ = ["name"]