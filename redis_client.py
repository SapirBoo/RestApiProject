import os
from redis import Redis

def get_redis():
    print("REDIS_URL =", os.getenv("REDIS_URL"))                                                                                                 
    return Redis.from_url(os.getenv("REDIS_URL"))