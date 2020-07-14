import jwt
from math import floor
import datetime
from .config import JWT_SECRET

def signJWT(payload: dict) -> str:
    payload["expires"] = currentTimeUnix() + (2 * 60 * 60)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decodeJWT(token: str) -> dict:
    try:
        payload = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return None if currentTimeUnix() >= payload["expires"] else payload
    except:
        return None

def currentTimeUnix() -> int:
    return int(floor(datetime.datetime.now(datetime.timezone.utc).timestamp()))