from location import Location


class Bin:
    def __init__(self, id: str, location: Location, max_capacity: float, waste_type: list[str], priority: int = 0):
        self.id = id
        self.location = location
        self.max_capacity = max_capacity
        self.current_capacity = max_capacity
        self.waste_type = waste_type
        self.priority = priority
    
    def empty(self):
        self.current_capacity = self.max_capacity
        return
