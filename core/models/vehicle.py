from waste import Waste
from segregation_plant import SegregationPlant
from processing_plant import ProcessingPlant
from bin import Bin

class Vehicle:
    def __init__(self, id: str, route_no: int, max_capacity: float, waste_types: list[str]):
        self.id = id
        self.route_no = route_no
        self.max_capacity = max_capacity
        self.available_capacity = max_capacity
        self.waste_types = waste_types
        self.current_location = None
        self.destination = None
        self.carrying_wastes: list[str] = []

    
    def collectFromBin(self, bin: Bin, waste: Waste):
        if self.available_capacity < waste.volume:
            print("Truck capacity exceeded")
            return
        if "unclassified" not in self.waste_types:
            print("Wrong truck")
            return
        
        bin.current_capacity = bin.max_capacity
        self.available_capacity -= waste.volume
        self.carrying_wastes.append(waste.id)


    def collectFromSeg(self, segPlant: SegregationPlant, waste: Waste):
        if waste.volume > self.available_capacity:
            print("Truck capacity not sufficient")
            return
        
        if waste.waste_type not in self.waste_types:
            print("Incompatible waste types")
            return
        
        segPlant.available_capacity = segPlant.max_capacity
        self.available_capacity -= waste.volume
        self.carrying_wastes.append(waste.id)
    

    def dumpToSeg(self, segPlant: SegregationPlant):
        if segPlant.available_capacity > self.max_capacity - self.available_capacity:
            print("Segregation plant capacity exceeding")
            return
        
        segPlant.available_capacity -= (self.max_capacity - self.available_capacity)
        self.available_capacity = self.max_capacity
        self.carrying_wastes.clear()

    
    def dumpToProc(self, procPlant: ProcessingPlant):
        if procPlant.available_capacity < self.max_capacity - self.available_capacity:
            print("Processing plant capacity exceeding")
            return
        
        if len(self.waste_types) != 1 or  procPlant.type not in self.waste_types:
            print("Wrong plant") 
            return
        
        for id in self.carrying_wastes:
            procPlant.processWaste(id)

        self.carrying_wastes.clear()
        self.available_capacity = self.max_capacity
