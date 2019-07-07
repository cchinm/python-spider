from celery import Celery
from practical.proxy import db

cele = Celery(__name__)
cele.config_from_object("config")

redis_conn = db.RedisHandler()