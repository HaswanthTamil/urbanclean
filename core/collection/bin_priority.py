from models.bin import Bin
from utils.storage import *
from utils.path import *
'''10.emergency
 highly populated/slums
 commercial area
tourists spots
 schools/colleges 
urban locality
govt buildings
private companies
industry

'''

'''import data from json'''
'''raw bin-load->compare loc.id->compare with location type->assign pripority->priority bins'''
datarawbin = []
datalocation = []
datafinal = []

load_json(LOCATION_DATA, datalocation)
load_json(RAW_BIN_DATA, datarawbin)

for bin in datarawbin:
    for location in datalocation:
        if bin["location_id"] == location["id"]:

            if location["location_type"] == "emergency":
                bin["priority"] = 10

            elif location["location_type"] == "populated":
                bin["priority"] = 9

            elif location["location_type"] == "commercial":
                bin["priority"] = 8

            elif location["location_type"] == "tourist":
                bin["priority"] = 7

            elif location["location_type"] == "school":
                bin["priority"] = 6

            elif location["location_type"] == "urban-loc":
                bin["priority"] = 5

            elif location["location_type"] == "govt-building":
                bin["priority"] = 4

            elif location["location_type"] == "private-corp":
                bin["priority"] = 3

            else:
                bin["priority"] = 1   # default priority

            datafinal.append(bin)
datafinal.sort(key=lambda x: x["priority"], reverse=True)
save_json(PRIORITY_BIN_DATA,datafinal)   
 
                            
                        
