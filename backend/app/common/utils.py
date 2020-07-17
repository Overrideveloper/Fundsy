import jwt
from math import floor
import datetime
import json
from .config import JWT_SECRET

def sign_jwt(payload: dict) -> str:
    payload["expires"] = current_time_unix() + (2 * 60 * 60)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return None if current_time_unix() >= payload["expires"] else payload
    except:
        return None

def current_time_unix() -> int:
    return int(floor(datetime.datetime.now(datetime.timezone.utc).timestamp()))

def convert_datetime_to_unix_timestamp(_datetime) -> int:
    return int(floor(_datetime.timestamp()))
