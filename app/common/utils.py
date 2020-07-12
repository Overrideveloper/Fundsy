import jwt
import time
from datetime import date, timedelta
from .config import JWT_SECRET

def signJWT(payload: dict) -> str:
    payload["expires"] = time.mktime((date.today() + timedelta(days=7)).timetuple())
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decodeJWT(token: str) -> dict:
    try:
        payload = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])

        return None if time.mktime(date.today().timetuple()) >= payload["expires"] else payload
    except:
        return None
