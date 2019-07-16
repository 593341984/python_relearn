# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-08"


class HealthCheck(object):

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(HealthCheck, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self._server = []

    def addServer(self):
        self._server.append('server 1')
        self._server.append('server 2')
        self._server.append('server 3')
        self._server.append('server 4')

    def changeServer(self):
        self._server.pop()
        self._server.append('server 5')


h1 = HealthCheck()
h2 = HealthCheck()

h1.addServer()
print("Schedule health check for server (1)..")

for i in range(4):
    print('checking ', h1._server[i])

h2.changeServer()

print("Schedule health check for server (2)..")

for i in range(4):
    print('checking ', h2._server[i])

from abc import ABCMeta, abstractmethod