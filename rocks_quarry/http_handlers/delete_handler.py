import json
import rocksdb

from rocks_quarry.db_utils import visitors

class DeleteHandler:
    def __init__(self, database):
        self.database = database

    def delete_children(self, key, it):
        class KeyBuilder:
            def __init__(self):
                # Delete ourself too!
                self.result = []

            def add_child(self, name, child):
                self.result.extend(child.get_result())

            def visit(self, name, next_value):
                self.result.append(name)

            def visit_container(self, name, next_value):
                print(f"Visting container:{name}")
                self.result.append(name)

            def get_result(self):
                return self.result

        def create_builder():
            return KeyBuilder()

        return visitors.children_visitor(key, it, create_builder)

    def handle_collection(self, key):
        it = self.database.iterkeys()
        it.seek(key)
        result = self.delete_children(key.decode("utf-8"), it)

        if not result:
            return None

        return result.get_result()

    def bulk_delete(self, to_delete):
        batch = rocksdb.WriteBatch()
        for item in to_delete:
            batch.delete(item.encode())

        self.database.write(batch)
        return len(to_delete)

    def handle_request(self, key):
        result = None

        if key and key[-1] ==  b'/'[0]:
            result = self.handle_collection(key)
        else:
            find = self.database.get(key)
            if  find:
                result = [key.decode("utf-8")]

        if not result:
            return (404, b"Key not found")

        num = self.bulk_delete(result)
        return (200, '{"total": %u, "deleted" : %s}' % (num, json.dumps(result)))
