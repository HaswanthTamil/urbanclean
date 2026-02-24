import random
from datetime import datetime
from utils.storage import load_json   # type: ignore

PREFIX_MAP = {
    "waste": "WASTE",
    "seg_plant": "SEG-PLANT",
    "proc_plant": "PROC-PLANT",
    "truck": "TRUCK",
    "bin": "BIN",
    "location": "LOC"
}


def generate_id(entity_type: str, json_path: str) -> str:
    # PREFIX-DDMMYYYY-RANDOMNUMBER
   
    prefix = PREFIX_MAP.get(entity_type.lower())
    if not prefix:
        raise ValueError(f"Invalid entity type: {entity_type}")

    date_part = datetime.now().strftime("%d%m%Y")

    existing_ids = _get_existing_ids(json_path)

    while True:
        random_part = random.randint(10000, 99999)
        new_id = f"{prefix}-{date_part}-{random_part}"

        if new_id not in existing_ids:
            return new_id


def _get_existing_ids(json_path: str) -> set[str]:
    try:
        data: list = load_json(json_path) # type: ignore
        return {item["id"] for item in data} # type: ignore
    except Exception:
        return set()
