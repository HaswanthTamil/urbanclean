from location import Location


class SegregationPlant:
    def __init__(self, id: str, location: Location, max_capacity: float, accuracy: float):
        self.id = id
        self.location = location
        self.max_capacity = max_capacity
        self.available_capacity = max_capacity
        self.accuracy = accuracy
        self.is_operational = True
    