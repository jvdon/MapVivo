import mysql.connector

import vivo_dns

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cache"
)

# MapIVivo DB


def search():
    pass


def add():
    pass


def delete():
    pass


def check_status():
    pass


def update():
    pass


def close() -> None:
    db.close()
