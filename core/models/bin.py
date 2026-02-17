from location import Location


class Bin:
    def __init__(self, id: str, location: Location, capacity: float, current_level: float, waste_type: list[str], priority: int = 0):
        self.id = id
        self.location = location
        self.capacity = capacity
        self.current_level = current_level
        self.waste_type = waste_type
        self.priority = priority
