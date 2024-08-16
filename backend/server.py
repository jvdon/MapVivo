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

# Project
import cache
import vivo_dns
import utils


app = Flask(__name__)

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
    if len(produtos) > 0:
        return jsonify(produtos), 200
    else:
        return jsonify({"error": "Nenhuma rota cadastrada"}), 404


@app.get("/dns/search/<produto>")
def dns_search(produto: str):
    produto, status = vivo_dns.search(produto)
    if status is True:
        return jsonify(produto), 200
    else:
        return jsonify({"error": "Rota não encontrada"}), 404


@app.post("/dns/add")
def dns_add():
    name = request.form["name"]
    address = request.form["address"]

    result, status = vivo_dns.add(name, address)

    return jsonify({"message": result}), 200 if status == True else 404


@app.delete("/dns/delete")
def dns_delete():
    index = request.args["id"]
    msg, status = vivo_dns.delete(index)

    return jsonify({"status": "ok" if status is True else "Fail"}), (
        200 if status == True else 404
    )


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
    cliente, status = cache.get(cliente=cliente, produto=produto.replace(" ", "_"))
    if status == True:
        return jsonify(cliente), 200
    else:
        return (
            jsonify({"status": "Error", "message": f"Oops something went wrong"}),
            500,
        )


# PRODUTO | CLIENTE | DATA


@app.post("/cache/save")
def save():
    cliente = str(request.json["cliente"]).upper()
    produto = str(request.json["produto"]).upper().replace(" ", "_")
    contents = request.json["contents"]

    if cache.save(cliente, produto, contents) == True:
        return (
            jsonify(
                {
                    "status": "Okay",
                    "message": f"Contents added to cache with key {cliente}",
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"status": "Error", "message": f"Oops something went wrong"}),
            500,
        )


# END REGION


# REGION DASHBOARD (API)


@app.get("/api/ping/<server>")
def ping(server: str):
    respTime, status = utils.ping(server)
    ok = status == True
    response = jsonify(
        {"status": "Ok" if ok else "Fail", "time": respTime if ok else -1}
    )

    vivo_dns.changePing(server, respTime)

    response.status_code == 200 if ok else 500
    return response


@app.get("/api/usage")
def checkUsage():
    size, statusStorage = utils.getUsage()
    cpu, statusCpu = utils.getCPU()
    ram, statusRam = utils.getRAM()

    response = jsonify(
        {
            "storage": {
                "status": "Ok" if statusStorage else "Fail",
                "value": size if statusStorage else -1,
            },
            "ram": {
                "status": "Ok" if statusRam else "Fail",
                "value": ram if statusRam else -1,
            },
            "cpu": {
                "status": "Ok" if statusCpu else "Fail",
                "value": cpu if statusCpu else -1,
            },
        }
    )

    return response, 200


# END REGION

app.run(host="0.0.0.0", port=5000)
