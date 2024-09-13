import requests
from faker import Faker
from datetime import datetime as datetime
import concurrent.futures

import cleanup

mock_url = "http://mock:5100/users/%s/products"
back_url = "http://nginx:8080"
faker = Faker()
format = "%d/%m/%Y %H:%M:%S"


def fetchUsers():
    url = f"{back_url}/updatable/all"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            body = r.json()
            print(body)
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
    update_url = f"{back_url}/updatable/update"
    payload = {"contents": content}
    try:
        r = requests.post(url, json=payload)
        print("Status Cache:", r.status_code)
        if r.status_code == 200:
            print("Cache atualizado")
            ok = cleanup.deleteClient(id)
            if ok:
                print(f"[{datetime.now().strftime(format)}] Cliente {id} Deletado")
            else:
                print(f"[{datetime.now().strftime(format)}] Erro ao deletar cliente {id}")

            # up_payload = {
            #     "user_id": id,
            #     "contents": {
            #         "in_cache": True,
            #         "last_seen": datetime.now().strftime("%d/%m/%Y"),
            #     },
            # }
            # ru = requests.put(update_url, json=up_payload)
            # if ru.status_code == 200:
            #     print(f"[{datetime.now().strftime(format)}] Updated clients database")
            # else:
            #     print(
            #         f"[{datetime.now().strftime(format)}] Unable to update clients DB: {ru.status_code}"
            #     )
        else:
            print(f"[{datetime.now().strftime(format)}]Unable to update cache...")

    except:
        print(f"[{datetime.now().strftime(format)}] Unable to connect to the backend")


def process_client(client):
    user_id = client["user_id"]
    products = fetchProducts(user_id)
    if len(products) > 0:
        saveData(user_id, products)


def main():
    print(f"[{datetime.now().strftime(format)}] Starting connector...")

    clients = fetchUsers()
    print(f"[{datetime.now().strftime(format)}] Got {len(clients)} users")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_client, client) for client in clients]

        # Optionally, wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Fetch result to catch exceptions
            except Exception as e:
                print(f"An error occurred: {e}")
