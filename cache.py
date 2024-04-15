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
    #! Add ID column to the table if createId is True
    table += f" {name}_id INTEGER PRIMARY KEY AUTO_INCREMENT,\n" if createId is True else ""
    
    for key in contents:
        item = contents[key]
        #? If the item is not a dictionary or a list, create a normal table column
        if (not (isinstance(item, dict) or isinstance(item, list))):
            #* Add ID column if 'id' is in the contents but not in the table definition
            if (contents.__contains__("id") and not table.__contains__("id")):
                table += f"id INTEGER PRIMARY KEY AUTO_INCREMENT,\n" if createId is True else ""

            #* Add the column definition to the table based on the type of the item
            table += f" {key} {table_types[type(item).__name__]} {'PRIMARY KEY AUTO_INCREMENT' if (str(key).__contains__('id') == True and not str(table).__contains__('PRIMARY KEY') ) else ''},\n"
        #? If the item is a dictionary, create a new sub-table and link it with the main table
        if (isinstance(item, dict)):
            #* Created a new table to house the anormal item
            create_table(f"SUB_{key}_{name}",
                        contents=contents[key], isSub=True)
        #? If the item is a list, take the first item, create a new sub-table, and link it with the main table
        elif (isinstance(item, list)):
            #* Created a new table to house the anormal item
            create_table(f"SUB_{key}_{name}",
                        contents=contents[key][0], isSub=True)

    return table

#! CRIA UMA NOVA TABELA


tables = []


def create_table(table_name: str, contents, isSub: bool = False):
    #! Determine if an ID column should be created based on the table name
    createId = (table_name.find("SUB") >= 0)

    #! Initialize the table creation SQL statement
    table = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    
    #! Populate the table with columns using the populate_table function
    sub_table = populate_table(table_name, table, contents, createId=createId)
    
    #! If it's a sub-table, add foreign key constraints linking it to the main table
    if (isSub):
        sub_table += f"{'_'.join(table_name.split('_')[2:])}_id INTEGER, \n"
        sub_table += f"FOREIGN KEY ({'_'.join(table_name.split('_')[2:])}_id) REFERENCES {'_'.join(table_name.split('_')[2:])}(id),\n"

    #! Format the table creation SQL statement
    table_cols = str(sub_table).split("\n")
    table_cols[-2] = table_cols[-2].replace(",", "")
    table = '\n'.join(table_cols)
    table += ");"

    print(table)

    #! Add the SQL statement to the list of tables
    tables.append(table)


def addTables():
    print("Creating table: ")

    #! Reverse the order of tables in the list
    tables.reverse()
    
    #! Create a cursor for database operations
    cursor = db.cursor()

    #! Iterate through tables and execute creation SQL statements
    for table in tables:
        print(table)
        cursor.execute(table)

    #! Clear the tables list after creating all tables
    tables.clear()

    #! Close the cursor
    cursor.close()

    #! Commit changes to DB
    db.commit()


#! BUSCA A TABELA <table_name> NA LISTA DE TABELAS DO BANCO


def search_tables(table_name):
    
    cursor = db.cursor()
    cursor.execute(
        f"SELECT table_name, table_schema from information_schema.tables where table_schema = 'cache' and table_name = '{table_name}' order by table_name;")
    table = cursor.fetchone()
    cursor.close()
    return (not (table is None))


#! INSERT INTO TABLE the client content;
def save(table, contents: dict):
    id = 0

    #! REGULAR TABLE

    filteredKeys = [key for key in contents if not (
        isinstance(contents[key], dict) or isinstance(contents[key], list) or key == "id")]

    parsedValues = ["'%s'" % item for item in contents.values() if not (
        isinstance(item, dict) or isinstance(item, list))][1:]

    sql = f"INSERT INTO {table} ({', '.join(filteredKeys)}) VALUES ({', '.join(parsedValues)});\n"
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)

    #! Get last inserted row id
    id = cursor.lastrowid
    # cursor.execute("SELECT LAST_INSERT_ID();")
    # id = cursor.fetchone()[0]
    print(id)
    cursor.close()

    #! SUB Tables
    for key in contents:
        item = contents[key]
        #! IF item is TYPE DICT
        if (isinstance(item, dict)):
            parsedValues = ["'%s'" % item for item in dict(item).values()]
            parsedValues.append("'%s'" % id)
            sql = f"INSERT INTO SUB_{key}_{table} ({', '.join(item.keys())}, {table}_id) VALUES ({', '.join(parsedValues)});\n"

            print(sql)

            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()
        #! IF item is TYPE LIST
        elif (isinstance(item, list)):
            for line in list(contents[key]):
                #? Turn values into a list that can be parsed to the DB
                parsedValues = ["'%s'" % item for item in dict(line).values()]
                #? Appends the id to the pa
                parsedValues.append("'%s'" % id)
                sql = f"INSERT INTO SUB_{key}_{table} ({', '.join(line.keys())}, {table}_id) VALUES ({', '.join(parsedValues)});\n"

                print(sql)

                cursor = db.cursor()
                cursor.execute(sql)
                cursor.close()

    db.commit()


def fetch(produto, cliente):
    #! Create cursors
    cursor = db.cursor()
    dictCursor = db.cursor(dictionary=True) # Returns DICT instead of tuple

    #! Get tables matching the product name from the database schema 'cache'

    cursor.execute(
        f"SELECT table_name from information_schema.tables where table_schema = 'cache' and table_name LIKE '%{produto}%' order by table_name;")
    tabs = cursor.fetchall()
    
    #! Split tables between main and sub Tables
    mainTable = [ t[0] for t in tabs if (t[0].__contains__("SUB_") == False) ][0]
    subTables = [ t[0] for t in tabs if (t[0].__contains__("SUB_")) ]

    #! Query the main table for items related to the client
    result = {}
    sql = f" SELECT * FROM {mainTable} WHERE nome = '{cliente}' LIMIT 1" # MAIN SELECT
    
    #* Execute the query and fetch the data
    dictCursor.execute(sql) 
    mainResult = dictCursor.fetchone() 
    
    # Appends results to main object
    result.update(mainResult)

    #? Fetch data from sub tables related to the main table entry
    for sub in subTables:
        sql = f"SELECT * FROM {sub} WHERE {mainTable}_id = {result['id']}"
        dictCursor.execute(sql)
        subResult = dictCursor.fetchall()
        
        #* Clean up the purely database-related IDs from the sub-result
        for res in subResult:
            res.pop(f"{mainTable}_id")
            res.pop(f"{sub}_id")
        
        #* If there's only one dictionary in the sub-result list, convert it into a dictionary
        if( len(subResult) == 1  ):
            subResult = subResult[0]

        #! Append sub-result to the main result object
        result[f"{sub.split('_')[1]}"] = subResult

    #! Close 
    cursor.close()
    dictCursor.close()
    

    return result

def close():
    # Closes the DB connection
    db.close()



# contents = {
#     "id": 10,
#     "nome": "Marcelo Resende",
#     "idade": 10,
#     "servicos": [
#         {
#             "nome": "Pós controle 20Gb",
#             "info": "Vivo pos controle",
#             "valor": 300,
#         },
#         {
#             "nome": "Pós controle 5Gb",
#             "info": "Vivo pos controle",
#             "valor": 300,
#         },
#     ],
#     "endereco": {
#         "rua": "Rua dos bobos",
#         "numero": 0,
#         "CEP": 666
#     }
# }


# if(search_tables("TABLE_VIVO_MOBILE") == False):
# create_table("TABLE_VIVO_MOBILE", contents)

# addTables()

# else:
#     print("Tables exist")


# save("TABLE_VIVO_MOBILE", contents)


# fetch(produto="VIVO_MOBILE", cliente="Marcelo Resende")