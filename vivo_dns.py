from mysql.connector import connect

import utils

db = connect(
    host="localhost",
    user="root",
    password="root",
    database="vivo"
)

"""
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        ping FLOAT DEFAULT 0
    );
"""

# MapIVivo DB

def getAll():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        produtos  = cursor.fetchall()
        cursor.close()
        return produtos, True
    except:
        return "Unable to fetch microsserviços", False

def search(nome_produto:str):
    sql = "SELECT * FROM produtos WHERE nome = %s SORT BY ping"
    try:
        cursor = db.cursor()
        cursor.execute(sql, (nome_produto, ))
        produto = cursor.fetchall()
        cursor.close()
        return produto[0], True
    except:
        return "Microsservice not found", False

def add(nome, addr):
    ping, status = utils.ping(addr)
    sql = "INSERT INTO produtos VALUES (%s, %s, %s)"
    cursor = db.cursor()
    try:
        cursor.execute(sql, (nome, addr, ping if status is True else -1,))
        return "Microsservice added", True
    except:
        return "Unable to add new microsservice", False

def delete():
    pass

def check_status(nome_produto:str):
    sql = "SELECT status FROM produtos WHERE nome = %s LIMIT 1"
    cursor = db.cursor()
    cursor.execute(sql, (nome_produto, ))
    status = cursor.fetchone()
    cursor.close()
    return status

def changeAddr(nome, addr):
    sql = "UPDATE SET address = %s  FROM produtos WHERE nome = %s"
    cursor = db.cursor()
    try:
        cursor.execute(sql, (addr, nome,))
        return "Microsservice added", True
    except:
        return "Unable to add new microsservice", False

def changePing(addr, ping):
    ping, status = utils.ping(addr)
    sql = "UPDATE SET ping = %s  FROM produtos WHERE address = %s"
    cursor = db.cursor()
    try:
        cursor.execute(sql, (ping if status is True else -1, nome,))
        return "Microsservice added", True
    except:
        return "Unable to add new microsservice", False

def close() -> None:
    db.close()
