
def children_visitor(key : str, it, visitor_factory):
    visitor = visitor_factory()

    next_val = Wrapper(it)
    while next_val.next() != None and next_val.key().startswith(key):
        next_key = next_val.key()

        # Assumption: anything ending with "/" has no data.
        # This simplifies the search, since we can skip over it.

        if next_key.endswith("/"):
            # Recursive case


            # FIGURE OUT HOW TO GET THE NAME HERE PROPERLY GRRR.
            # Maybe we should just pass the full name in. Do the basename in get?
            visitor.visit_container(next_key, next_val.value())

            next_visitor = children_visitor(next_key, it, visitor_factory)
            if next_visitor:
                visitor.add_child(next_key, next_visitor)

        else:
            # Base case -- no children
            visitor.visit(next_key, next_val.value())

    if next_val.first_found_key() and next_val.first_found_key().startswith(key):
        return visitor
    else:
        return None

class Wrapper:
    def __init__(self, iter):
        self.iter = iter
        self.cur_item = None
        self.first_key = None

    def first_found_key(self):
        return self.first_key

    def next(self):
        self.cur_item = next(self.iter, None)
        if not self.first_key and self.cur_item:
            self.first_key = self.key()

        return self.cur_item

    def key(self):
        return self.cur_item[0].decode("utf-8")
    def value(self):
        if len(self.cur_item) <= 1:
            return None
        else:
            return self.cur_item[1]
