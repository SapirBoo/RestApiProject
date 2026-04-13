from rq import Queue
from redis_client import get_redis

email_queue = Queue("emails", connection=get_redis())