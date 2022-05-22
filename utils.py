import json

from enum import Enum, auto
from typing import Dict, Any


class Operations(Enum):
    BADGES = auto()
    BEERS = auto()
    CHECKINS = auto()
    INFO = auto()


def save_to_json(filename: str = 'untappd_data', data: Dict[str, Any] = None) -> None:
    with open(f"data/{filename}.json", "w") as f:
        json.dump(data, f)


def load_json(filename: str = '') -> Dict:
    with open(f"data/{filename}.json", "r") as f:
        return json.load(f)
