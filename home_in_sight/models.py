from .data import get_county

class Location:
    __slots__ = ["id", "address", "street", "city", "state", "zipcode", "county", "longitude", "latitude", "type"]

    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None, type=None):
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

    @staticmethod
    def split_address(address:str) -> tuple:
        """Takes address as a string and returns a tuple of its composite sections"""
        address = address.split(", ")
        street = address[0]
        city = address[1]
        statezip = address[2].split(" ")
        state = statezip[0]
        zipcode = statezip[1] if len(statezip)>1 else None
        return (street, city, state, zipcode)

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
            #! etc.

        }

        return json

    @staticmethod
    def from_json(json): ...

    @staticmethod
    def calc_distance(pointA:"Location", pointB:"Location", units="metric") -> float:
        "Given the coordinates of two locations, returns the distance in KM unless otherwise specified"
        # uses the pythagorean theorem (i.e. 2D geometry) to calculate a linear distance as opposed to distance along a great circle but this is fine for short distances
        delta_lat = pointA.latitude - pointB.latitude
        delta_lng = pointA.longitude - pointB.longitude
        delta = pow(pow(delta_lat, 2)+pow(delta_lng, 2), 0.5)
        distance = Location.degree_to_km(delta)
        return round(distance, 2)

    @staticmethod
    def degree_to_km(degree:float) -> float:
        km_per_degree = 111
        return round(degree * km_per_degree, 2)
    
    @staticmethod
    def km_to_mi(KM:float) -> float:
        mi_per_km = 0.621371
        return round(KM * mi_per_km, 2)

    def __repr__(self):
        return f"{self.address}"
        

class Property(Location):
    __slots__ = ["FIPS_code", "zpid", "url", "images", "use_code", "beds", "baths", "property_area", "lot_area", "year_built", "year_updated", "POIs"]
    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None, FIPS_code=None, county=None, zpid=None, url=None, images=[], use_code=None, beds=None, baths=None, property_area=None, lot_area=None, year_built=None, year_updated=None):
        super().__init__(street, city, state, zipcode, longitude, latitude, type="Property")
        self.FIPS_code = FIPS_code
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

        self._set_county()

        from .data import POI_types
        self.POIs = {Type: [] for Type in POI_types}

    def _set_county(self):
        self.county = get_county(self.FIPS_code)

    def json(self):
        json = {
            "id": self.id,
            "zpid": self.zpid,
            "url": self.url,
            "location": {
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "zip code": self.zipcode,
                "FIPS_code": self.FIPS_code,
                "county": self.county,
                "address": self.address,
                "longitude": self.longitude,
                "latitude": self.latitude
            },
            "type": "Property",
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

    def add_POI(self, Type:str, POI:"POI"):
        points = self.POIs[Type]
        points.append(POI) if POI not in points else None

class POI(Location):
    __slots__ = ["name", "place_id", "distance"]

    def __init__(self, street, city, state, zipcode=None, longitude=None, latitude=None, name=None, place_id=None):
        super().__init__(street, city, state, zipcode, longitude, latitude)
        self.name = name
        self.place_id = place_id

    @staticmethod
    def from_json(json):
        candidate = json.get("candidates")[0]
        formatted_address = candidate.get("formatted_address")
        street, city, state, zipcode = Location.split_address(formatted_address)
        geometry = candidate.get("geometry")
        location = geometry.get("location")
        longitude = location.get("lng")
        latitude = location.get("lat")
        name = candidate.get("name")
        place_id = candidate.get("place_id")

        return POI(street, city, state, zipcode, longitude, latitude, name, place_id)

    def __repr__(self):
        return f"{self.name} - {self.address}"

    def __str__(self):
        return f"{self.name} - {self.address}"