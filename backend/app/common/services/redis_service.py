import json
from redis import StrictRedis
from typing import Any
from ..config import REDIS_HOST, REDIS_PORT

redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def get(key: str) -> Any:
    data = redis.get(key)

    return json.loads(data) if data is not None else data

def set(key: str, data: Any):
    redis.set(name=key, value=json.dumps(data))
        
def delete(key: str):
    redis.delete(key)
