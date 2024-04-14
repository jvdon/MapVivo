import mysql.connector

table_types = {
    "str": "VARCHAR(255)",
    "int": "INTEGER",
    "float": "DOUBLE",
    "bool": "BOOLEAN",
}

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cache"
)

#! Popula a tabela com colunas


def populate_table(name: str, table, contents: dict, createId=True):

    table += f" {name}_id INTEGER PRIMARY KEY AUTO_INCREMENT,\n" if createId is True else ""
    for key in contents:
        item = contents[key]
        #! SE NÂO FOR LISTA OU DICT CRIE A TABELA NORMALMENTE
        if (not (isinstance(item, dict) or isinstance(item, list))):
            if (contents.__contains__("id") and not table.__contains__("id")):
                table += f"id INTEGER PRIMARY KEY AUTO_INCREMENT,\n" if createId is True else ""

            table += f" {key} {table_types[type(item).__name__]} {'PRIMARY KEY AUTO_INCREMENT' if (str(key).__contains__('id') == True and not str(table).__contains__('PRIMARY KEY') ) else ''},\n"
        #! SE FOR DICT, ABRA O DICIONARIO CRIE UMA NOVA TABLE E LINK COM A PRINCIPAL
        if (isinstance(item, dict)):
            create_table(f"SUB_{key}_{name}",
                         contents=contents[key], isSub=True)
        #! SE FOR LIST, PEGUE O PRIMEIRO ITEM, CRIE UMA NOVA TABLE E LINK COM A PRINCIPAL
        elif (isinstance(item, list)):
            create_table(f"SUB_{key}_{name}",
                         contents=contents[key][0], isSub=True)

    return table

#! CRIA UMA NOVA TABELA


tables = []


def create_table(table_name: str, contents, isSub: bool = False):
    createId = (table_name.find("SUB") >= 0)

    table = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    sub_table = populate_table(table_name, table, contents, createId=createId)
    if (isSub):
        sub_table += f"{'_'.join(table_name.split('_')[2:])}_id INTEGER, \n"
        sub_table += f"FOREIGN KEY ({'_'.join(table_name.split('_')[2:])}_id) REFERENCES {'_'.join(table_name.split('_')[2:])}(id),\n"

    table_cols = str(sub_table).split("\n")
    table_cols[-2] = table_cols[-2].replace(",", "")
    table = '\n'.join(table_cols)
    table += ");"

    print(table)

    tables.append(table)


def addTables():
    print("Creating table: ")
    tables.reverse()
    cursor = db.cursor()
    for table in tables:
        print(table)
        cursor.execute(table)

    cursor.close()
    db.commit()


# * BUSCA A TABELA <table_name> NA LISTA DE TABELAS DO BANCO


def search_tables(table_name):

    cursor = db.cursor()
    cursor.execute(
        f"SELECT table_name, table_schema from information_schema.tables where table_schema = 'cache' and table_name = '{table_name}' order by table_name;")
    table = cursor.fetchone()
    cursor.close()
    return (not (table is None))


# TODO: INSERT INTO TABLE VALUES value;
def save(table, contents: dict):
    id = 0
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cache"
    )

    # REGULAR TABLE

    keyes = [key for key in contents if not (
        isinstance(contents[key], dict) or isinstance(contents[key], list) or key == "id")]

    vales = ["'%s'" % item for item in contents.values() if not (
        isinstance(item, dict) or isinstance(item, list))][1:]

    sql = f"INSERT INTO {table} ({', '.join(keyes)}) VALUES ({', '.join(vales)});\n"
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.execute("SELECT LAST_INSERT_ID();")
    id = cursor.fetchone()[0]
    print(id)
    cursor.close()

    for key in contents:
        item = contents[key]
        if (isinstance(item, dict)):
            vales = ["'%s'" % item for item in dict(item).values()]
            vales.append("'%s'" % id)
            sql = f"INSERT INTO SUB_{key}_{table} ({', '.join(item.keys())}, {table}_id) VALUES ({', '.join(vales)});\n"

            print(sql)

            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()
        elif (isinstance(item, list)):
            for line in list(contents[key]):
                # print(line)
                vales = ["'%s'" % item for item in dict(line).values()]
                vales.append("'%s'" % id)
                sql = f"INSERT INTO SUB_{key}_{table} ({', '.join(line.keys())}, {table}_id) VALUES ({', '.join(vales)});\n"

                print(sql)

                cursor = db.cursor()
                cursor.execute(sql)
                cursor.close()

    db.commit()


def close():
    db.close()


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


# if(search_tables("TABLE_VIVO_MOBILE") == False):
# create_table("TABLE_VIVO_MOBILE", contents)

# addTables()
# else:
#     print("Tables exist")


save("TABLE_VIVO_MOBILE", contents)
