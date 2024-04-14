import mysql.connector

from flask import Flask, request, jsonify, make_response, redirect
import cache

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vivo"
)

# CLIENTE | PRODUTO


@app.get("/fetch")
def fetch():

    return "<h1>ONLINE</h1>"

# DATA | PRODUTO


@app.get("/save")
def save():
    produto = request.json["produto"]
    contents = {
        "id": 10,
        "nome": "Marcelo Resende",
        "idade": 10,
        "servicos": [
            {
                "nome": "Pós controle 20Gb",
                "info": "Vivo pos controle",
                "valor": 300
            },
            {
                "nome": "Pós controle 5Gb",
                "info": "Vivo pos controle",
                "valor": 300
            },
        ],
        "endereco": {
            "rua": "Rua dos bobos",
            "numero": 0,
            "CEP": 666
        }
    }

    if(cache.search_tables(produto)):
        # INSERT ITEMS IN TABLE

    else:
        # CREATE TABLES
        cache.create_table(produto, contents)


app.run(host="0.0.0.0", port=5000)
