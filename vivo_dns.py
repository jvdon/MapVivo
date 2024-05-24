import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dns"
)

# MapIVivo DB

def getAll():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos  = cursor.fetchall()
    cursor.close()
    return produtos
    

def search(nome_produto:str):
    sql = "SELECT * FROM produtos WHERE nome = %s LIMIT 1"
    cursor = db.cursor()
    cursor.execute(sql, (nome_produto, ))
    produto = cursor.fetchone()
    cursor.close()
    return produto


def add():
    pass


def delete():
    pass


def check_status(nome_produto:str):
    sql = "SELECT status FROM produtos WHERE nome = %s LIMIT 1"
    cursor = db.cursor()
    cursor.execute(sql, (nome_produto, ))
    status = cursor.fetchone()
    cursor.close()
    return status



def update():
    pass


def close() -> None:
    db.close()
