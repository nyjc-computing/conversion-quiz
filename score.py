from typing import List, Dict


import os
import psycopg2
from psycopg2.extras import RealDictCursor

import utils.time


TABLE_NAME = "scores"


def get_connection():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    return psycopg2.connect(url)


def load() -> List[Dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id SERIAL PRIMARY KEY,
                    timestamp TEXT,
                    name TEXT,
                    bin_score INTEGER,
                    dec_score INTEGER,
                    hex_score INTEGER
                )
            """)
            cur.execute(f"SELECT timestamp, name, bin_score, dec_score, hex_score FROM {TABLE_NAME} ORDER BY id DESC")
            return [dict(row) for row in cur.fetchall()]


def save(scores: List[Dict]) -> None:
    """Replace all scores in the database with the provided list."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {TABLE_NAME}")
            for score in scores:
                cur.execute(
                    f"""
                    INSERT INTO {TABLE_NAME} (timestamp, name, bin_score, dec_score, hex_score)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        score["timestamp"],
                        score["name"],
                        score["bin_score"],
                        score["dec_score"],
                        score["hex_score"]
                    )
                )
        conn.commit()

def record(name: str, bin_score: int, dec_score: int, hex_score: int) -> Dict:
    return {
        "timestamp": utils.time.get_timestamp(),
        "name": name,
        "bin_score": bin_score,
        "dec_score": dec_score,
        "hex_score": hex_score,
    }


def add_score(name: str, bin_score: int, dec_score: int, hex_score: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {TABLE_NAME} (timestamp, name, bin_score, dec_score, hex_score)
                VALUES (%s, %s, %s, %s, %s)
            """,
            (
                utils.time.get_timestamp(),
                name,
                bin_score,
                dec_score,
                hex_score
            ))
        conn.commit()


def delete_score(index: int) -> bool:
    """
    Delete the score at the given index (0-based, most recent first).
    Returns True if deleted, False if index out of range.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT id FROM {TABLE_NAME} ORDER BY id DESC")
            ids = [row["id"] for row in cur.fetchall()]
            if 0 <= index < len(ids):
                cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (ids[index],))
                conn.commit()
                return True
    return False
