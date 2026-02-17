from typing import Literal

class Waste:

    WasteType = Literal["bio-degradable", "inert", "metal", "e-waste", "medical", "recyclable", "unclassified","other"]

    def __init__(self,waste_type :WasteType,id :str,volume :float):
        self.waste_type=waste_type
        self.id=id
        self.volume=volume

    def toDict(self) -> dict: # type: ignore
        return {
            "id": self.id,
            "waste_type": self.waste_type,
            "volume": self.volume
        } # type: ignore
