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


def getCPU():
    cursor = db.cursor(dictionary=True)
    sql = "SET GLOBAL innodb_monitor_enable='cpu%';"
    cursor.execute(sql)
    cursor.fetchall()

    sql = "SELECT TRUNCATE(sum(AVG_COUNT) * 100, 2) as CPU from information_schema.INNODB_METRICS WHERE name LIKE 'cpu%';"
    cursor.execute(sql)
    cpu = cursor.fetchone()
    return cpu, (cpu == "null")


def getRAM():
    cursor = db.cursor(dictionary=True)
    sql = "SELECT FORMAT_BYTES(SUM(current_alloc)) as RAM FROM sys.x$memory_global_by_current_bytes;"
    cursor.execute(sql)
    ram = cursor.fetchone()
    return ram, True


def ping(server):
    try:
        response_time = ping3.ping(server)
        if response_time is not None:
            return response_time * 1000, True
        else:
            return -1, False
    except Exception as e:
        return f"Error: {e}", False


def close():
    db.close()
