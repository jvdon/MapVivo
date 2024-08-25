import shelve
import sys

clientes = shelve.open("./db/clientes")


"""obj = {
    user_id: number,
    in_cache: bool,
    last_seen: date
}
"""


# Read All
def getAll():
    try:
        return [clientes[key] for key in clientes.keys()], True
    except:
        return [], False


# Read
def get(cliente:str):
    index = cliente
    print(index)
    try:
        if index not in clientes:
            return "Client Not Found", False
        else:
            return clientes[index], True
    except Exception as e:
        return "Error opening DB", False


# Check Exists
def exists(cliente:str):
    index = cliente
    try:
        return index in clientes
    except:
        return False


# Write


def save(cliente:str, content):
    index = cliente
    try:
        clientes[index] = content
        return True
    except Exception as e:
        print(e)
        return False


# Update


def update(user_id:str, content):
    try:
        old = dict(clientes[user_id])
        old.update(content)

        clientes[user_id] = old
        return True
    except:
        return False


# Delete
def delete(cliente):
    index = cliente

    try:
        del clientes[index]
        return True
    except:
        return False


def usage():
    return sys.getsizeof(clientes)
