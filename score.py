from datetime import datetime
import json
from typing import List, Dict

DBNAME = "scores.json"

def load() -> List[Dict]:
    with open("scores.json", "r") as f:
        return json.load(f)

def save(scores: List[Dict]) -> None:
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

def record(name: str, bin_score: int, dec_score: int) -> Dict:
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "bin_score": bin_score,
        "dec_score": dec_score,
    }

def add_score(name: str, bin_score: int, dec_score: int) -> None:
    scores = load()
    scores.append(record(name, bin_score, dec_score))
    save(scores)
