import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="vivo"
)

table_types = {
    "str": "VARCHAR(255)",
    "int": "INTEGER",
    "float": "DOUBLE"
}

tables = []

def populate_table(name, table, contents, createId = True):
    table += f" {name}_id INTEGER PRIMARY KEY,\n" if createId is True else ""
    for key in contents:
        item = contents[key]
        if(not (isinstance(item, dict) or isinstance(item, list))):
            table += f" {key} {table_types[type(item).__name__]},\n"
        elif (isinstance(item, dict)):
            create_table(f"SUB_{key}_{name}", contents=contents[key])
        elif (isinstance(item, list)):
            create_table(f"SUB_{key}_{name}", contents=contents[key][0])
    table_cols = str(table).split("\n")
    
    table_cols[-2] = table_cols[-2].replace(",", "")
    table = '\n'.join(table_cols)
    return table

def create_table(table_name, contents):
    table = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    table = populate_table(table_name, table, contents, createId=(len(tables) != 0))
    table += ");"
    tables.append(table)


contents = [{
    "id": 10,
    "nome": "Jose Luiz Datena",
    "CPF":12345678910,
    "servico": [
        {
            "nome": "FIBRA",
            "description": "FIBRA 300Mbps",
            "valor": 500
        },
        {
            "nome": "FIBRA",
            "description": "FIBRA 500Mbps",
            "valor": 300
        }
    ],
    "combo": {
        "a": "netflix",
        "b": "fibra"
    },
},
{
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
]
counter = 0
names = ["TABLE_VIVO_FIBRA", "TABLE_VIVO_MOBILE"]
for content in contents:
    print(f"Bloco #{counter}")
    create_table(table_name = names[counter], contents=content)
    counter += 1

for table in tables:
    print("Creating table: ")
    print(table)
    cursor = mydb.cursor()
    cursor.execute(table)
    cursor.close()

    mydb.commit()

mydb.close()

