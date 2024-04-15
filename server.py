import mysql.connector

from flask import Flask, request, jsonify, make_response, redirect
import cache

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

#Register the function to be called on exit
atexit.register(close_running_threads)
#start your process

# CLIENTE | PRODUTO

@app.get("/cache/fetch")
def fetch():
    
    return "<h1>ONLINE</h1>"

# DATA | PRODUTO


@app.get("/cache/save")
def save():
    produto = str(request.json["produto"])
    table = produto if produto.__contains__("TABLE_") else "TABLE_%s" % produto

    print(table)
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

    if(cache.search_tables(table)):
        # INSERT ITEMS IN TABLE
        cache.save(table=table, contents=contents)
    else:
        # CREATE TABLES
        cache.create_table(produto, contents)
        cache.addTables()


app.run(host="0.0.0.0", port=5000)
