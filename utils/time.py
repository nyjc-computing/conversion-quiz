from datetime import datetime

def utcnow() -> datetime:
    return datetime.now(datetime.UTC)

def get_timestamp() -> str:
  """Return the current timestamp in ISO format."""
  return utcnow().isoformat()

def get_datetime(timestamp: str) -> datetime:
  """Return the datetime object corresponding to the given timestamp."""
  return datetime.fromisoformat(timestamp)
