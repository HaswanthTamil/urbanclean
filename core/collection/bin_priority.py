from utils.storage import load_json, save_json
from utils.path import LOCATION_DATA, RAW_BIN_DATA, PRIORITY_BIN_DATA
from models.location import Location

PRIORITY_MAP = {
    "emergency": 10,
    "populated": 9,
    "commercial": 8,
    "tourist": 7,
    "school": 6,
    "urban-loc": 5,
    "govt-building": 4,
    "private-corp": 3,
    "industry": 2
}


def generate_priority_bins():
    raw_bins: list[object] = load_json(RAW_BIN_DATA) 
    locations: list[object] = load_json(LOCATION_DATA) 

    location_map: dict[str, Location] = {loc["id"]: loc for loc in locations} # type: ignore

    priority_bins: list[dict] = [] 

    for bin_data in raw_bins: 
        location: Location = location_map.get(bin_data["location_id"]) # type: ignore

        if not location:
            continue  # skip invalid mapping safely

        location_type = location.location_type
        priority = PRIORITY_MAP.get(location_type, 1)

        # create new dict (avoid mutating original)
        updated_bin: dict = { 
            **bin_data, # type: ignore
            "priority": priority
        }

        priority_bins.append(updated_bin)

    # sort high → low priority
    priority_bins.sort(key=lambda x: x["priority"], reverse=True) 

    save_json(PRIORITY_BIN_DATA, priority_bins) 
