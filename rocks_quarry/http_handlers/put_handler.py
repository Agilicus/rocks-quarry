class PutHandler:
    def __init__(self, database):
        self.database = database

    def handle_request(self, key, data):
        self.database.put(key, data)
        return 200
