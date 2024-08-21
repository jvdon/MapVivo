import utils
from datetime import datetime
import shelve
import sys

# MapIVivo DB

dns = shelve.open("./cache/dns")

def getAll():
    try:
        return [dns[key] for key in dns.keys()], True
    except:
        return [], False


def search(nome_produto: str):

    try:
        dnss = list(dns[nome_produto])
        dnss.sort()
        return dnss, True
    except:
        return "Microsservice not found", False


def products():
    try:
        return [{key: dns[key]["nome"]} for key in dns.keys()], True
    except:
        return [], False


def add(nome, addr):
    ping, status = utils.ping(addr)

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
    try:
        del dns[addr]
        return f"#{addr} Deleted", True
    except:
        return "Error deleting", False

def changePing(addr, ping):
    try:
        dns[addr]["ping"] = ping
        return "Microservice updated", True
    except Exception as e:
        return f"Unable to update microservice {e}", False


def close() -> None:
    dns.close()

def usage():
    return sys.getsizeof(dns)