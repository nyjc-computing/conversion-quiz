from typing import List, Dict

from replit import db

import utils.time

DBNAME = "scores"

def copy(scores: List[Dict]) -> List[Dict]:
    """Return a copy of the given list of scores.

    Replit DB returns wrappers around db entries, which we want to 
    avoid passing around to prevent inadvertent mutation.
    """
    return [dict(score) for score in scores]

def load() -> List[Dict]:
    if not db.get(DBNAME):
        db[DBNAME] = []
    return copy(db[DBNAME])

def save(scores: List[Dict]) -> None:
    raise NotImplementedError

def record(name: str, bin_score: int, dec_score: int, hex_score: int) -> Dict:
    return {
        "timestamp": utils.time.get_timestamp(),
        "name": name,
        "bin_score": bin_score,
        "dec_score": dec_score,
        "hex_score": hex_score,
    }

def add_score(name: str, bin_score: int, dec_score: int, hex_score: int) -> None:
    if not db.get(DBNAME):
        db[DBNAME] = []
    scores = db[DBNAME]
    scores.append(
        record(name, bin_score, dec_score, hex_score)
    )
    # db[DBNAME] = scores

def delete_score(index: int) -> bool:
    scores = db[DBNAME]
    if 0 <= index < len(scores):
        del scores[index]
        return True
    return False
