import requests
from set_interval import setInterval
from faker import Faker

mock_url = "http://localhost:5100/users/%s/products"
back_url = "http://localhost:5000"
faker = Faker()


def fetchUsers(id):
    url = mock_url % id
    print(url)
    try:
        r = requests.get(url=url)
        return r.json() if r.status_code == 200 else []
    except:
        return []


def saveData(id, content):
    url = f"{back_url}/cache/save"
    payload = {"cliente": id, "contents": content}
    try:
        r = requests.post(url, json=payload)
        print(r.status_code, r.json())
    except:
        print("Unable to save data")


def connect():
    user_id = faker.uuid4()
    print("Fetching mock data")
    # fetched = fetchUsers(user_id)
    # print(fetched)

    print("Saving it to the MapViVO cache")
    # saveData(user_id, fetched)


id = setInterval(5, connect)

setInterval(1 * 30, id.cancel)
