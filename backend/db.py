from mysql.connector import connect
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

if DEBUG:
    db = connect(host="localhost", user="root", password="root", database="vivo")
else:
    db = connect(host="mysql", user="root", password="root", database="vivo")
