from mysql.connector import connect
import ping3

db = connect(
    host="localhost",
    user="root",
    password="root",
    database="vivo"
)

def getUsage():
    try:
        sql = "select sum((data_length+index_length)/1024) AS KB from information_schema.tables;"
        cursor = db.cursor()
        cursor.execute(sql)

        size = cursor.fetchone()
        return size[0], True
    except:
        return -1, False

def ping(server):
    try:
        response_time = ping3.ping(server)
        if response_time is not None:
            return response_time * 1000, True
        else:
            return "No response", False
    except Exception as e:
        return f"Error: {e}", False
    
def close():
    db.close()