class Vehicle:
    def __init__(self, id: str, route_no: int, max_capacity: float, waste_types: list[str]):
        self.id = id
        self.route_no = route_no
        self.max_capacity = max_capacity
        self.available_capacity = max_capacity
        self.waste_types = waste_types
        self.current_location = None
        self.destination = None
