class SegregationPlant:
    def __init__(self, id, location, capacity, accuracy):
        self.id = id
        self.location = location
        self.capacity = capacity
        self.available_capacity = capacity
        self.accuracy = accuracy
        self.is_operational = True
