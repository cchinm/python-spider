# author: Z.M Z

import abc
import redis
import time

class DBbaseHandler:

    @abc.abstractmethod
    def delete(self, key, name):
        pass

    @abc.abstractmethod
    def deletemany(self, name, *key):
        pass

    @abc.abstractmethod
    def add(self, value, key, name):
        pass


    def addmany(self, name, *kvs):
        for k, v in kvs:
            self.add(v, k, name)

    @abc.abstractmethod
    def all(self, name):
        pass

    @abc.abstractmethod
    def has(self, key, name):
        pass


class RedisHandler(DBbaseHandler):

    def __init__(self, url='redis://127.0.0.1:6379/0', name=None):
        self.__conn = redis.Redis().from_url(url=url)
        self.name = name

    def delete(self, key, name):
        name = self.name or name
        return self.__conn.execute_command("ZREM", name, key)

    def deletemany(self, name, *key):
        name = self.name or name
        return self.__conn.execute_command("ZREM", name, *key)

    def add(self, value, key, name):
        return self.__conn.execute_command("ZADD", name, value, key)

    def all(self, name):
        return self.__conn.zscan(name)

    def has(self, key, name):
        return self.__conn.zscore(name, key) is not None