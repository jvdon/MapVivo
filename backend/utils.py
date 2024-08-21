from mysql.connector import connect
import ping3
import psutil
import vivo_dns as dns
import cache
import requests
from threading import Event, Thread


mock_url = "http://localhost:5000/users/%s/products"


def getUsage():
    try:
        size = cache.usage() + dns.usage()
        return size, True
    except:
        return -1, False


def getRAM():
    ram = psutil.virtual_memory()
    return ram.used / (1024**2), True


def ping(server):
    try:
        response_time = ping3.ping(server)
        if response_time is not None:
            return response_time * 1000, True
        else:
            return 1000, False
    except Exception as e:
        return f"Error: {e}", False


def fetchData():

    print("Fetching")