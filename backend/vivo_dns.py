import utils
from datetime import datetime
import shelve
import sys

# MapIVivo DB


def open_cache(file_path):
    try:
        return shelve.open(file_path, writeback=True)
    except Exception as e:
        print(f"Error opening shelve file: {e}")
        return None


# Check cache access
def checkCache():
    return open_cache("./db/dns") != None


def getAll():
    dns = open_cache("./db/dns")
    try:
        return [dns[key] for key in dns.keys()], True
    except:
        return [], False


def search(nome_produto: str):
    dns = open_cache("./db/dns")
    try:
        dnss = list(dns[nome_produto])
        dnss.sort()
        return dnss, True
    except:
        return "Microsservice not found", False


def products():
    dns = open_cache("./db/dns")
    try:
        return [{key: dns[key]["nome"]} for key in dns.keys()], True
    except:
        return [], False


def add(nome, addr):
    ping, status = utils.ping(addr)
    dns = open_cache("./db/dns")

    try:
        time = datetime.now()
        dns[addr] = {
            "nome": nome,
            "address": addr,
            "ping": ping,
            "checked_on": time,
        }
        return "Microsservice added", True
    except Exception as e:
        return f"Unable to add new microsservice {e}", False


def delete(addr):
    dns = open_cache("./db/dns")
    try:
        del dns[addr]
        return f"#{addr} Deleted", True
    except:
        return "Error deleting", False


def changePing(addr, ping):
    dns = open_cache("./db/dns")
    try:
        dns[addr]["ping"] = ping
        return "Microservice updated", True
    except Exception as e:
        return f"Unable to update microservice {e}", False


def close() -> None:
    dns = open_cache("./db/dns")
    dns.close()


def usage():
    return sys.getsizeof(dns)
