class Vehicle:
    def __init__(self, id, route_no, capacity, waste_types):
        self.id = id
        self.route_no = route_no
        self.capacity = capacity
        self.available_capacity = capacity
        self.waste_types = waste_types
        self.current_location = None
        self.destination = None
