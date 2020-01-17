class Property:
    __slots__ = ["zpid", "street", "zipcode", "city", "state", "longitude", "latitude", "url", "images", "use_code", "beds", "baths", "property_area", "lot_area", "year_built", "year_updated"]
    def __init__(self):
        pass

    def json(self):
        json = {
            "zpid": self.zpid,
            "url": self.url,
            "address": {
                "street": self.street,
                "city": self.city,
                "state": self.state,
                "zip code": self.zipcode
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