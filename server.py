import mysql.connector

from flask import Flask, request, jsonify, make_response, redirect

import cache
import vivo_dns

import atexit

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vivo"
)


def close_running_threads():
    print("Closing DB Connection...")
    cache.close()


# Register the function to be called on exit
atexit.register(close_running_threads)
# start your process


@app.get("/dns/all")
def dns_all():
    produtos = vivo_dns.getAll()
    if len(produtos) > 0:
        return jsonify(produtos), 200
    else:
        return jsonify({
            "error": "Nenhuma rota cadastrada"
        }), 404


@app.get("/dns/search/<produto>")
def dns_search(produto: str):
    produto = vivo_dns.search(produto)
    if produto is not None:
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


app.run(host="0.0.0.0", port=5000)
