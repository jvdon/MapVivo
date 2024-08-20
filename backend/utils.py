from mysql.connector import connect
import ping3
import os
import psutil

import cache
from db import db


def getUsage():
    try:
        size = cache.usage()
        return size, True
    except:
        return -1, False


def getRAM():
    ram = psutil.virtual_memory()
    print(ram.used)
    return ram.used / (1024**3), True


def ping(server):
    try:
        response_time = ping3.ping(server)
        if response_time is not None:
            return response_time * 1000, True
        else:
            return 1000, False
    except Exception as e:
        return f"Error: {e}", False


def close():
    db.close()
