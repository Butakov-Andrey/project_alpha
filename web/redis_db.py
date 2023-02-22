from config import settings
from redis import ConnectionPool, Redis

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = 0

redis_pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
redis_conn = Redis(connection_pool=redis_pool, decode_responses=True)
