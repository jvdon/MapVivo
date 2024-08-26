import shelve
import sys

import threading

cache_lock = threading.Lock()

import os


def open_cache(file_path):
    """Open the shelve file with writeback enabled."""
    with cache_lock:
        try:
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(
                    os.path.dirname(file_path)
                )  # Create directory if it does not exist
            return shelve.open(file_path, writeback=True)
        except Exception as e:
            print(f"Error opening shelve file: {e}")
            return None


# Check cache access
def checkCache():
    return open_cache("./cache/vivo") != None


# Read All
def getAll():
    with open_cache("./cache/vivo") as cache:
        if cache is None:
            return [], False
        try:
            return [{key: cache[key]} for key in cache.keys()], True
        except Exception as e:
            print(f"Error reading all entries: {e}")
            return [], False


# Read
def get(cliente):
    with open_cache("./cache/vivo") as cache:
        if cache is None:
            return "Error opening DB", False
        try:
            if cliente not in cache:
                return "File Not Found", False
            return cache[cliente], True
        except KeyError:
            return "File Not Found", False
        except Exception as e:
            print(f"Error retrieving entry: {e}")
            return "Error opening DB", False


# Check Exists
def exists(cliente):
    with open_cache("./cache/vivo") as cache:
        if cache is None:
            return False
        try:
            return cliente in cache
        except Exception as e:
            print(f"Error checking existence: {e}")
            return False


# Write


def save(cliente, content):
    with open_cache("./cache/vivo") as cache:
        if cache is None:
            return False
        try:
            cache[cliente] = content
            cache.sync()
            return True
        except Exception as e:
            print(f"Error saving entry: {e}")
            return False


# Update


def update(cliente, content):
    return save(cliente, content)


# Delete
def delete(cliente):
    with cache_lock:
        with open_cache("./cache/vivo") as cache:
            if cache is None:
                return False
            try:
                if cliente in cache:
                    del cache[cliente]
                    cache.sync()
                    return True
                else:
                    return False
            except KeyError:
                return False
            except Exception as e:
                print(f"Error deleting entry: {e}")
                return False
            finally:
                cache.close()


def usage():
    with open_cache("./cache/vivo") as cache:
        if cache is None:
            return "Error opening DB"
        return sys.getsizeof(cache)
