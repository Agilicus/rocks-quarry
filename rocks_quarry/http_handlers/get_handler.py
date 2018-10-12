import itertools
import json

from rocks_quarry.db_utils import visitors

class GetHandler:
    def __init__(self, database):
        self.database = database


    def find_children(self, key, it):
        class DictBuilder:
            def __init__(self):
                self.result = dict()

            def add_child(self, full_name, child):
                name = base_name(full_name)
                self.result[name] = child.get_result()

            def visit(self, full_name, next_value):
                name = base_name(full_name)
                self.result[name] = next_value.decode("utf-8")

            def visit_container(self, full_name, value):
                pass

            def get_result(self):
                return self.result

        def create_builder():
            return DictBuilder()

        return visitors.children_visitor(key, it, create_builder)

    def handle_collection(self, key):
        it = self.database.iteritems()
        it.seek(key)
        result = self.find_children(key.decode("utf-8"), it)

        if not result:
            return None
        else:
            return json.dumps(result.get_result())

    def handle_request(self, key):
        if key and key[-1] ==  b'/'[0]:
            result = self.handle_collection(key)
        else:
            result = self.database.get(key)

        if not result:
            return (404, b"key not found")

        return (200, result)

def base_name(full_name, sep = "/"):
    name = full_name[full_name.rfind(sep, 0, -1) + 1:]

    if name.endswith(sep):
        name = name[:-1]

    return name
