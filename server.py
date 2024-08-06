from flask import Flask, request, jsonify, make_response, redirect

import cache
import vivo_dns
import utils

import atexit


app = Flask(__name__)

def close_running_threads():
    print("Closing DB Connection...")
    cache.close()
    utils.close()


# Register the function to be called on exit
atexit.register(close_running_threads)
# start your process

@app.get("/dns/all")
def dns_all():
    produtos, status = vivo_dns.getAll()
    if status is True:
        return jsonify(produtos), 200
    else:
        return jsonify({
            "error": "Nenhuma rota cadastrada"
        }), 404


@app.get("/dns/search/<produto>")
def dns_search(produto: str):
    produto, status = vivo_dns.search(produto)
    if status is True:
        return jsonify(produto), 200
    else:
        return jsonify({
            "error": "Rota não encontrada"
        }), 404

# CLIENTE


@app.get("/cache/fetch/<cliente>")
def fetch(cliente: str):
    cliente, status = cache.get(cliente=cliente)
    if (status == True):
        return jsonify(cliente), 200
    else:
        return jsonify({
            "status": "Error",
            "message": f"Oops something went wrong"
        }), 500

# CLIENTE | DATA


@app.post("/cache/save")
def save():
    cliente = str(request.json["cliente"]).upper()
    contents = request.json["contents"]

    if (cache.save(cliente, contents) == True):
        return jsonify({
            "status": "Okay",
            "message": f"Contents added to cache with key {cliente}"
        }), 200
    else:
        return jsonify({
            "status": "Error",
            "message": f"Oops something went wrong"
        }), 500

@app.get("/dashboard/ping/<server>")
def ping(server: str):
    respTime, status = utils.ping(server)
    ok = (status == True)
    response = jsonify({
        "status": "Ok" if ok else "Fail",
        "time": respTime if ok else -1
    })

    vivo_dns.changePing(server, respTime)

    response.status_code == 200 if ok else 500
    return response

@app.get("/dashboard/usage")
def checkUsage():
    size, status = utils.getUsage()
    ok = (status == True)
    response = jsonify({
        "status": "Ok" if ok else "Fail",
        "time": size if ok else -1
    })

    response.status_code == 200 if ok else 500
    return response

app.run(host="0.0.0.0", port=5000)
