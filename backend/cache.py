import shelve
import sys

cache = shelve.open("./cache/vivo")


# Read All
def getAll():
    try:
        return [{key: cache[key]} for key in cache.keys()], True
    except Exception as e:
        return [], False


# Read
def get(cliente):
    index = cliente
    print(index)
    try:
        if index not in cache:
            return "File Not Found", False
        else:
            return cache[index], True
    except Exception as e:
        return "Error opening DB", False

# Check Exists
def exists(cliente):
    index = cliente
    try:
        return index in cache
    except:
        return False


# Write


def save(cliente, content):
    index = cliente
    try:
        cache[index] = content
        return True
    except:
        return False


# Update


def update(cliente, content):
    index = cliente
    try:
        cache[index] = content
        return True
    except:
        return False


# Delete
def delete(cliente):
    index = cliente

    try:
        del cache[index]
        return True
    except:
        return False


def usage():
    return sys.getsizeof(cache)
