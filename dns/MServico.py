class MServico:
    def __init__(self, id, client, product, api):
        self.id = id
        self.client = client
        self.product = product
        self.api = api

    #! Converts object into INSERT sql statement
    def toInsert(self):
        return f"INSERT INTO MServicos(client, product, name) VALUES  ('{self.client}', '{self.product}', '{self.api}');"

    #! Converts object into DELETE sql statement
    def toDelete(self):
        return f"DELETE FROM MServicos where id = {self.id};"
