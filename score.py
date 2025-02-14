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

def record(name: str, bin_score: int, dec_score: int) -> Dict:
    return {
        "timestamp": utils.time.get_timestamp(),
        "name": name,
        "bin_score": bin_score,
        "dec_score": dec_score,
    }

def add_score(name: str, bin_score: int, dec_score: int) -> None:
    db[DBNAME].append(record(name, bin_score, dec_score))
