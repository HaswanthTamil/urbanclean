
class Bin:
    def __init__(self, id, location, capacity, current_level, waste_type):
        self.id = id
        self.location = location
        self.capacity = capacity
        self.current_level = current_level
        self.waste_type = waste_type
        self.priority = 0
