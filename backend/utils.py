from mysql.connector import connect
import ping3
import os

import cache
from db import db


def getUsage():
    try:
        size = cache.usage()
        return size, True
    except:
        return -1, False


def getRAM():
    cursor = db.cursor(dictionary=False)
    sql = "SELECT FORMAT_BYTES(SUM(current_alloc)) as RAM FROM sys.x$memory_global_by_current_bytes;"
    cursor.execute(sql)
    ram = cursor.fetchone()
    return float(ram[0].replace("MiB", "")), True


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
