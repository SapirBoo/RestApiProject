import os
import ssl
from celery import Celery
from dotenv import load_dotenv


load_dotenv()
print("REDIS_URL =", os.getenv("REDIS_URL"))
REDIS_URL = os.environ["REDIS_URL"]

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.update(
    broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
    },

    result_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE
    }
)

celery.conf.imports = ("tasks",)

