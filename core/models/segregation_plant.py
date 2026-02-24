from location import Location
from waste import Waste
from utils.id_generator import generate_id
from utils.path import WASTE_DATA
from utils.storage import *

class SegregationPlant:

    def __init__(self, id: str, location: Location, accuracy: float, max_capacity: float):
        self.id = id
        self.location = location
        self.max_capacity = max_capacity
        self.available_capacity: float = max_capacity
        self.accuracy = accuracy
        self.is_operational = True


    # def dump(self, waste: Waste):

    #     if self.available_capacity < waste.volume:
    #         print("Plant capacity exceeded. Dumping failed")
    #         return
    #     else:
    #         self.available_capacity -= waste.volume
    #         remove_from_json(waste.id, WASTE_DATA)
    #         del waste


    def segregate(self) -> list[Waste]:
        total_waste = self.max_capacity - self.available_capacity

        bio_deg = Waste("bio-degradable", generate_id("waste", WASTE_DATA) , total_waste * 0.4)

        inert = Waste("inert", generate_id("waste", WASTE_DATA) , total_waste * 0.1)
        add_to_json(inert.toDict(), WASTE_DATA) # type: ignore

        metal = Waste("metal", generate_id("waste", WASTE_DATA) , total_waste * 0.05)
        add_to_json(metal.toDict(), WASTE_DATA) # type: ignore

        e_waste = Waste("e-waste", generate_id("waste", WASTE_DATA) , total_waste * 0.05)
        add_to_json(e_waste.toDict(), WASTE_DATA) # type: ignore

        medical = Waste("medical", generate_id("waste", WASTE_DATA) , total_waste * 0.05)
        add_to_json(medical.toDict(), WASTE_DATA) # type: ignore

        recyclable = Waste("recyclable", generate_id("waste", WASTE_DATA) , total_waste * 0.3)
        add_to_json(recyclable.toDict(), WASTE_DATA) # type: ignore

        other = Waste("other", generate_id("waste", WASTE_DATA) , total_waste * 0.05)
        add_to_json(other.toDict(), WASTE_DATA) # type: ignore

        return [bio_deg, inert, metal, e_waste, medical, recyclable, other]
        
