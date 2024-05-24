import shelve

cache = shelve.open("cache/vivo")


# Read
def get(cliente) -> str | bool:
    try:
        if cliente not in cache:
            return "File Not Found", False
        else:
            return cache[cliente], True
    except:
        return "Error opening DB", False


def exists(cliente):
    try:
        return (cliente in cache)
    except:
        return False

# Write


def save(cliente, content):
    try:
        cache[cliente] = content
        return True
    except:
        return False

# Update


def update(cliente, content):
    try:
        cache[cliente] = content
        return True
    except:
        return False


# Delete
def delete(cliente):
    try:
        del cache[cliente]
        return True
    except:
        return False
