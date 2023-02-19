from config import Settings
from redis import Redis

REDIS_HOST = Settings().REDIS_HOST
REDIS_PORT = Settings().REDIS_PORT
REDIS_DB = 0

redis_conn = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)
