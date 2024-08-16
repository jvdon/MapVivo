import shelve
import sys

cache = shelve.open("./cache/vivo")


# Read All
def getAll():
    try:
        return [{key: cache[key]} for key in cache.keys()], True
    except:
        return "Error opening DB", False


# Read
def get(cliente, produto):
    index = f"{cliente}_{produto}"
    print(index)
    try:
        if index not in cache:
            return "File Not Found", False
        else:
            return cache[index], True
    except Exception as e:
        return "Error opening DB", False


def exists(cliente, produto):
    index = f"{cliente}_{produto}"
    try:
        return index in cache
    except:
        return False


# Write


def save(cliente, produto, content):
    index = f"{cliente}_{produto}"
    try:
        cache[index] = content
        return True
    except:
        return False


# Update


def update(cliente, produto, content):
    index = f"{cliente}_{produto}"
    try:
        cache[index] = content
        return True
    except:
        return False


# Delete
def delete(cliente, produto):
    index = f"{cliente}_{produto}"

    try:
        del cache[index]
        return True
    except:
        return False


def usage():
    return sys.getsizeof(cache)
