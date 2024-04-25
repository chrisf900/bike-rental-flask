import os

import redis
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(".env")
db = SQLAlchemy()


REDIS_CONFIG = {
    "HOST": "redis",
    "PORT": 6379,
    "DATABASE": 0,
    "USERNAME": "default",
    "PASSWORD": os.environ["REDIS_PASSWORD"],
}


class RedisClient(object):

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=REDIS_CONFIG["HOST"],
            port=REDIS_CONFIG["PORT"],
            username=REDIS_CONFIG["USERNAME"],
            password=REDIS_CONFIG["PASSWORD"],
            decode_responses=True,
        )

    @property
    def conn(self):
        if not hasattr(self, "_conn"):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = redis.Redis(connection_pool=self.pool)
