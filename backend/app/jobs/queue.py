from rq import Queue
from redis import Redis
from app.config import settings

redis_conn = Redis.from_url(settings.redis_url)
queue = Queue("default", connection=redis_conn)


def enqueue(func_path: str, *args, **kwargs):
    return queue.enqueue(func_path, *args, **kwargs)
