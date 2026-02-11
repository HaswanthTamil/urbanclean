from enum import Enum

class WasteType(Enum):
    GENERAL = "general"
    PLASTIC = "plastic"
    ORGANIC = "organic"
    MEDICAL = "medical"

class LocationType(Enum):
    EMERGENCY = "emergency"
    NON_EMERGENCY = "non_emergency"
    PRIORITY = "priority"
