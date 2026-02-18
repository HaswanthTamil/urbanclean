from location import Location
from waste import Waste
from utils.storage import remove_from_json, findWaste
from utils.path import WASTE_DATA


class ProcessingPlant:

    def __init__(self, id :int,max_capacity :float, plant_type: str, location: Location, pollution_limit: int):
        self.id = id
        self.type = plant_type
        self.location = location
        self.max_capacity=max_capacity
        self.available_capacity=max_capacity
        self.pollution_limit = pollution_limit
        self.current_pollution = 0
        self.is_operational = True
    

    def processWaste(self, wasteID: str):
        waste: Waste = findWaste(wasteID, WASTE_DATA)
        if self.type != waste.waste_type:
            print("Incompatible waste type")
            return
        
        if waste.volume > self.available_capacity:
            print("Overload!")
            return
        
        if self.current_pollution + waste.pollution > self.pollution_limit:
            print("Waste is too hazardous to process here")
            return
        
        self.available_capacity -= waste.volume
        self.current_pollution += waste.pollution
        remove_from_json(waste.id, WASTE_DATA)
        del waste
        return
    

    def cleanPlant(self):
        self.available_capacity = self.max_capacity
        self.current_pollution = 0

    # def biodegradable(self,volume:float):
    #     if volume is greater than the biodegradable plant
    #     than the data,pass to next plant,and existing volume to
    #     if data from json compare,if greater,:
    #         return
    
    # def non_biodegradable(self,volume:float):
    #     waste_type=self.type
    
    #     if waste_type=="metal":
    #         if data from json compare,if greater,:
    #             return
    #             add to the data of this class
    #     if waste_type=="e-waste":
    #         if data from json compare,if greater,:
    #             return
    #            add to the data of this class 
    #     if waste_type=="medical":
    #         if data from json compare,if greater,:
    #             return
    #            add to the data of this class         
    #     if waste_type=="inert":
    #         if data from json compare,if greater,:
    #             return
    #             add to the data of this class    
    #     if waste_type=="others":
    #         if data from json compare,if greater,:
    #             return
    #            add to the data of this class    
    #     if waste_type=="recyclable":
    #         if data from json compare,if greater,:
    #             return
    #            add to the data of this class 
    

    # def output_towards_destination(self,volume :int):
    #     waste_type=self.type
    #     if waste_type in ["recylable","metal","e-waste"]:
    #         """pass to recycling factory,given volume,intoa truck
    #          with apt direction"""
    #     elif waste_type=="medical":
    #         """pass to medical recycle,given volume,intoa truck
    #          with apt direction"""  
    #     else:
    #         """pass to dumpyard,given volume,intoa truck
    #          with apt direction"""      



        




