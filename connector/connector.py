import requests
from faker import Faker

mock_url = "http://localhost:5100/users/%s/products"
back_url = "http://localhost:5000"
faker = Faker()


def fetchUsers():
    url = f"{back_url}/client/all"
    r = requests.get(url)
    # print(r.status_code, r.json())
    try:
        if r.status_code == 200:
            body = r.json()
            clients = body["contents"]
            return clients
        else:
            return []
    except Exception as e:
        return []


def fetchProducts(id):
    url = mock_url % id
    try:
        r = requests.get(url=url)
        return r.json() if r.status_code == 200 else []
    except:
        return []


def saveData(id, content):
    url = f"{back_url}/cache/save"
    update_url = f"{back_url}/client/update"
    payload = {"cliente": id, "contents": content}
    try:
        r = requests.post(url, json=payload)
        print("Status Cache:", r.status_code)
        if r.status_code == 200:
            up_payload = {
                "user_id": id,
                "contents": {
                    "in_cache": True,
                },
            }
            ru = requests.put(update_url, json=up_payload)
            print(ru.status_code, ru.text)
    except:
        print("Unable to save data")


def connect():
    user_id = faker.uuid4()
    print("Fetching mock data")
    # fetched = fetchUsers(user_id)
    # print(fetched)

    print("Saving it to the MapViVO cache")
    # saveData(user_id, fetched)

clients = fetchUsers()

for client in clients:
    user_id = client["user_id"]
    products = fetchProducts(user_id)
    print(user_id, products)
    if len(products) > 0:
        saveData(user_id, products)
