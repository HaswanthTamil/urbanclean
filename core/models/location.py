class Location:
    def __init__(self, id: str, name: str, lat: float, lon: float, location_type: str):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.location_type = location_type

    def toDict(self) -> dict: 
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "location_type": self.location_type
        }

# emergency
# populated
# tourist
# school
# urban-locality
# govt-building
# private-corp
# industry
# commercial
