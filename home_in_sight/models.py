class Location:
    __slots__ = ["id", "location", "address", "street", "city", "state", "zipcode", "longitude", "latitude", "type"]

    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None):
        self.id = None
        self.street = street # street address
        self.city = city
        self.state = state
        self.zipcode = zipcode

        self._set_address()

        self.longitude = longitude
        self.latitude = latitude
        
    def _set_address(self):
        self.address = f"{self.street}, {self.city}, {self.state} {self.zipcode}"

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
    __slots__ = ["FIPScounty", "county", "zpid", "url", "images", "use_code", "beds", "baths", "property_area", "lot_area", "year_built", "year_updated"]
    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None, FIPScounty=None, county=None, zpid=None, url=None, images=[], use_code=None, beds=None, baths=None, property_area=None, lot_area=None, year_built=None, year_updated=None):
        super().__init__(street, city, state, zipcode, longitude, latitude)
        self.FIPScounty = FIPScounty
        self.county = county
        self.zpid = zpid
        self.url = url
        self.images = images
        self.use_code = use_code
        self.beds = beds
        self.baths = baths
        self.property_area = property_area
        self.lot_area = lot_area
        self.year_built = year_built
        self.year_updated = year_updated

    def json(self):
        json = {
            "zpid": self.zpid,
            "url": self.url,
            "location": {
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "zip code": self.zipcode,
                "FIPScounty": self.FIPScounty,
                "county": self.county,
                "address": f"{self.street}, {self.city}, {self.state} {self.zipcode}",
                "longitude": self.longitude,
                "latitude": self.latitude
            },
            "images": [link for link in self.images],
            "use_code": self.use_code,
            "rooms": {
                "beds": self.beds,
                "baths": self.baths
            },            
            "size": {
                "property_area": self.property_area,
                "lot_area": self.lot_area
            },
            "year_built": self.year_built,
            "year_updated": self.year_updated

        }

        return json

class POI(Location):
    __slots__ = ["name", "place_id"]

    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None, name=None, place_id=None):
        super().__init__(street, city, state, zipcode, longitude, latitude)
        self.name = name,
        self.place_id = place_id