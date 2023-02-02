import config
from redis import Redis

redis_conn = Redis(
    host=config.settings.REDIS_HOST,
    port=config.settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)
