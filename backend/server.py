# Flask
from flask import (
    Flask,
    request,
    jsonify,
)
from flask_swagger_ui import get_swaggerui_blueprint
import atexit

from datetime import datetime


# Project
import cache
import vivo_dns
import utils
import clientes

import threading

app = Flask(__name__)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

thread_lock = threading.Lock()


def close_running_threads():

    print("Closing DB Connection...")


# Register the function to be called on exit
atexit.register(close_running_threads)

# start your process
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "MapVIVO"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# REGION DNS
@app.get("/dns/all")
def dns_all():
    produtos, status = vivo_dns.getAll()
    ok = (len(produtos) > 0) and status

    return jsonify(produtos), (200 if ok else 404)


@app.get("/dns/search/<produto>")
def dns_search(produto: str):
    produto, status = vivo_dns.search(produto.upper())

    return jsonify(
        {
            "ok": status,
            "content": produto if status else "Rota não encontrada",
        }
    ), (200 if status else 404)


@app.post("/dns/add")
def dns_add():
    name = str(request.json["name"]).upper()
    address = str(request.json["address"]).lower()

    result, status = vivo_dns.add(name, address)

    return jsonify({"message": result}), 200 if status == True else 404


@app.delete("/dns/delete")
def dns_delete():
    index = request.args["id"]
    msg, status = vivo_dns.delete(index)

    return jsonify({"ok": status}), (200 if status == True else 404)


@app.get("/dns/names")
def dns_products():
    produtos, status = vivo_dns.products()
    ok = (len(produtos) > 0) and status

    return jsonify(
        {
            "ok": ok,
            "content": produtos,
        }
    ), (200 if ok else 404)


# END REGION


# REGION CACHE


@app.get("/cache/all")
def cache_all():
    with thread_lock:
        result, status = cache.getAll()
    print(status)
    if len(result) > 0:
        return jsonify(result), 200
    else:
        return jsonify({"status": "No entries in cache"}), 404


@app.get("/cache/fetch/<cliente>")
def fetch(produto: str, cliente: str):
    with thread_lock:
        cliente, status = cache.get(
            cliente=cliente.upper(), 
            produto=produto.upper().replace(" ", "_")
        )
    if status == True:
        return jsonify(cliente), 200
    else:
        return (
            jsonify(
                {
                    "status": "Error",
                    "message": f"Oops something went wrong",
                }
            ),
            500,
        )


# PRODUTO | CLIENTE | DATA


@app.post("/cache/save")
def save():
    cliente = str(request.json["cliente"]).upper()
    contents = request.json["contents"]
    with thread_lock:
        ok = cache.save(cliente, contents)

    return jsonify(
        {
            "ok": ok,
            "message": (
                f"Contents added to cache with key {cliente}"
                if ok
                else f"Oops something went wrong"
            ),
        },
        200 if ok else 500,
    )


@app.delete("/cache/delete")
def delete_cache():
    user_id = str(request.args["user_id"])

    with thread_lock:
        ok = cache.delete(user_id)
    return f"{user_id} Deleted" if ok else "Unable to delete", 200 if ok else 400


# END REGION


# REGION Clientes
@app.get("/client/all")
def clientes_all():
    with thread_lock:
        clients, ok = clientes.getAll()
    return {
        "ok": ok,
        "contents": clients,
    }, (200 if ok else 404)


@app.post("/client/add")
def clientes_add():
    user_id = str(request.json["user_id"])
    in_cache = False
    last_seen = datetime.now()

    with thread_lock:
        ok = clientes.save(
            user_id,
            {
                "user_id": user_id,
                "in_cache": in_cache,
                "last_seen": last_seen.strftime("%d/%m/%Y"),
            },
        )

    return jsonify(
        {
            "ok": ok,
            "message": (
                "Cliente adicionado" if ok else "Não foi possível adicionar o cliente"
            ),
        }
    ), (200 if ok else 400)


@app.delete("/client/delete")
def cliente_delete():
    user_id = str(request.args["user_id"])
    with thread_lock:
        ok = clientes.delete(user_id)
    return f"{user_id} Deleted" if ok else "Unable to delete", 200 if ok else 400


@app.put("/client/update")
def cliente_update():
    user_id = str(request.json["user_id"])
    contents = dict(request.json["contents"])

    contents.update({"user_id": user_id})

    with thread_lock:
        ok = clientes.update(user_id, contents)

    return "Updated" if ok else "Unable to update", 200 if ok else 400


@app.get("/client/search")
def client_search():
    user_id = str(request.args["user_id"])
    with thread_lock:
        result, ok = clientes.get(user_id)
    return jsonify({"ok": ok, "message": result}), 200 if ok else 404


# END REGION


# REGION DASHBOARD (API)
@app.get("/api/ping/<server>")
def ping(server: str):
    with thread_lock:
        respTime, ok = utils.ping(server)

    response = jsonify(
        {
            "server": server,
            "time": respTime,
        }
    )

    with thread_lock:
        result, status = vivo_dns.changePing(server, respTime)
    print(result, status)
    response.status_code == 200 if ok else 500
    return response


@app.get("/api/usage")
def checkUsage():
    size, statusStorage = utils.getUsage()
    with thread_lock:
        ram, statusRam = utils.getRAM()

    response = jsonify(
        {
            "status": (statusRam and statusStorage),
            "ram": ram if statusRam else -1,
            "storage": size if statusStorage else -1,
        }
    )

    return response, 200


# END REGION

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
