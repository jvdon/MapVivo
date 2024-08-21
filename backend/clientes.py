import shelve
import sys

clientes = shelve.open("./cache/clientes")


# obj = 100

# Read All
def getAll():
    try:
        return [clientes[key] for key in clientes.keys()], True
    except:
        return "Error opening DB", False


# Read
def get(cliente):
    index = cliente
    print(index)
    try:
        if index not in clientes:
            return "File Not Found", False
        else:
            return clientes[index], True
    except Exception as e:
        return "Error opening DB", False

# Check Exists
def exists(cliente):
    index = cliente
    try:
        return index in clientes
    except:
        return False


# Write


def save(cliente, content):
    index = cliente
    try:
        clientes[index] = content
        return True
    except:
        return False


# Update


def update(cliente, content):
    index = cliente
    try:
        clientes[index] = content
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
