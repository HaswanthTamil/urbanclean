class ProcessingPlant:
    def __init__(self, id, plant_type, location, pollution_limit):
        self.id = id
        self.type = plant_type
        self.location = location
        self.pollution_limit = pollution_limit
        self.current_pollution = 0
        self.is_operational = True
