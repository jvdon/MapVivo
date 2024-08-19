# Flask
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    send_file,
)
from flask_swagger_ui import get_swaggerui_blueprint
import atexit

from flask_cors import CORS, cross_origin


# Project
import cache
import vivo_dns
import utils


app = Flask(__name__)

cors = CORS(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"


def close_running_threads():
    print("Closing DB Connection...")
    utils.close()


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

    return jsonify(
        {
            "ok": ok,
            "content": produtos if ok else "Nenhuma rota cadastrada",
        }
    ), (200 if ok else 404)


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
    result, status = cache.getAll()
    print(status)
    if len(result) > 0:
        return jsonify(result), 200
    else:
        return jsonify({"status": "No entries in cache"}), 404


@app.get("/cache/fetch/<produto>/<cliente>")
def fetch(produto: str, cliente: str):
    cliente, status = cache.get(
        cliente=cliente.upper(), produto=produto.upper().replace(" ", "_")
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
    produto = str(request.json["produto"]).upper().replace(" ", "_")
    contents = request.json["contents"]

    ok = cache.save(cliente, produto, contents)

    return jsonify(
        {
            "ok": ok,
            "message": (
                f"Contents added to cache with key {cliente}"
                if ok
                else f"Oops something went wrong"
            ),
        },
        200,
    )


# END REGION


# REGION DASHBOARD (API)


@app.get("/api/ping/<server>")
def ping(server: str):
    respTime, ok = utils.ping(server)

    response = jsonify({"ok": ok, "time": respTime})

    result, status = vivo_dns.changePing(server, respTime)
    print(result, status)
    response.status_code == 200 if ok else 500
    return response


@app.get("/api/usage")
def checkUsage():
    size, statusStorage = utils.getUsage()
    ram, statusRam = utils.getRAM()

    response = jsonify(
        [
            {
                "name": "RAM",
                "status": statusRam,
                "value": size if statusStorage else -1,
            },
            {
                "name": "STORAGE",
                "status": statusRam,
                "value": ram if statusRam else -1,
            },
        ]
    )

    return response, 200


# END REGION

app.run(host="0.0.0.0", port=5000)
