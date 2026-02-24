import random
from models.bin import Bin

def receive_bin_data(bins: list[Bin]) -> list[dict]: # type: ignore
    """
    Pretend IoT push.
    Returns payload list:
    [
        {"bin_id": "...", "current_volume": 83.2},
        ...
    ]
    """

    payload: list[dict] = [] # type: ignore

    for bin_obj in bins:
        # Random fill between 20% and 100%
        fill_percentage = random.uniform(20, 100)

        current_volume = (
            fill_percentage / 100
        ) * bin_obj.max_capacity

        payload.append({ # type: ignore
            "bin_id": bin_obj.id,
            "current_volume": round(current_volume, 2)
        })

    return payload # type: ignore



def update_bins(bins: list[Bin], sensor_payload: list[dict]): # type: ignore
    """
    Updates in-memory bin objects with incoming IoT data.
    """

    bin_map = {b.id: b for b in bins}

    for reading in sensor_payload: # type: ignore
        bin_obj = bin_map.get(reading["bin_id"]) # type: ignore

        if bin_obj:
            bin_obj.current_capacity = min(
                reading["current_volume"], # type: ignore
                bin_obj.max_capacity
            )
