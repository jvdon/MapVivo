import utils
from db import db
from datetime import datetime

# MapIVivo DB


def getAll():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos ORDER BY ping ASC;")
        produtos = cursor.fetchall()
        cursor.close()
        return produtos, True
    except:
        return "Unable to fetch microsserviços", False


def search(nome_produto: str):
    sql = "SELECT * FROM produtos WHERE nome = %s ORDER BY ping ASC;"
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql, (nome_produto,))
        produto = cursor.fetchall()
        cursor.close()
        return produto, True
    except:
        return "Microsservice not found", False

def products():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT nome FROM produtos")
        produtos = cursor.fetchall()
        cursor.close()
        if(len(produtos) <= 0):
            return f"Nenhum nome cadastrado", False
        else:
            return produtos, True
    except Exception as e:
        return f"Unable to fetch names {e}", False

def add(nome, addr):
    ping, status = utils.ping(addr)
    sql = "INSERT INTO produtos (nome, address, ping) VALUES (%s, %s, %s)"
    cursor = db.cursor()
    try:
        cursor.execute(
            sql,
            (
                nome,
                addr,
                ping if status is True else -1,
            ),
        )
        return "Microsservice added", True
    except Exception as e:
        return "Unable to add new microsservice", False


def delete(produto_id):
    cursor = db.cursor()
    sql = "DELETE FROM produtos where id = %s"

    try:
        cursor.execute(sql, (produto_id,))
        return f"#{produto_id} Deleted", True
    except:
        return "Error deleting", False


def check_status(nome_produto: str):
    sql = "SELECT status FROM produtos WHERE nome = %s LIMIT 1"
    cursor = db.cursor()
    cursor.execute(sql, (nome_produto,))
    status = cursor.fetchone()
    cursor.close()
    return status


def changeAddr(nome, addr):
    sql = "UPDATE produtos SET address = %s WHERE nome = %s"
    cursor = db.cursor()
    try:
        cursor.execute(
            sql,
            (
                addr,
                nome,
            ),
        )
        return "Microservice updated", True
    except:
        return "Unable to update microservice", False


def changePing(addr, ping):
    sql = "UPDATE produtos SET ping = %s WHERE address = %s"
    cursor = db.cursor()
    try:
        cursor.execute(
            sql,
            (
                ping,
                addr,
            ),
        )
        return "Microservice updated", True
    except Exception as e:
        return f"Unable to update microservice {e}", False


def close() -> None:
    db.close()
