class FakeFB:
    def __init__(self):
        self.db = dict()

    def put(self, key, value):
        self.db[key] = value

    def get(self, key):
        return self.db.get(key, None)

    def delete(self, key):
        self.db.pop(key, None)

    def iteritems(self):
        class SortedItemIterator:
            def __init__(self, input_dict):
                self.to_iterate = list(sorted(input_dict.items()))
                self.iterator = iter(self.to_iterate)

            def seek(self, key):
                while self.to_iterate and self.to_iterate[0][0] < key:
                    self.to_iterate.pop(0)
                self.iterator = iter(self.to_iterate)

            def __iter__(self):
                return self.iterator

            def __next__(self):
                return next(self.iterator)

        return SortedItemIterator(self.db)

    def iterkeys(self):
        class SortedKeysIterator:
            def __init__(self, input_dict):
                self.to_iterate = list(sorted(input_dict.keys()))
                self.iterator = iter(self.to_iterate)

            def seek(self, key):
                while self.to_iterate and self.to_iterate[0] < key:
                    self.to_iterate.pop(0)
                self.iterator = iter(self.to_iterate)

            def __iter__(self):
                return self.iterator

            def __next__(self):
                return next(self.iterator)

        return SortedKeysIterator(self.db)

    def write(self, batch):
        for op, key, value in batch:
            if op == "Put":
                self.put(key, value)
            elif op == "Delete":
                self.delete(key)
