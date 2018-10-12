
def children_visitor(key : str, it, visitor_factory):
    """
    Visits children of a '/' separated hierachy. The first search must
    start with '/'
    """
    if not key.endswith("/"):
        return None

    return container_children_visitor(key, it, visitor_factory)[0]


def container_children_visitor(key : str, it, visitor_factory):
    visitor = visitor_factory()

    next_val = Wrapper(it)

    while next_val.next() != None and next_val.key().startswith(key):
        next_key = next_val.key()

        # Assumption: anything ending with "/" has no data.
        # This simplifies the search, since we can skip over it.
        if next_key.endswith("/"):
            # Recursive case
            visitor.visit_container(next_key, next_val.value())

            next_visitor, skipped = container_children_visitor(next_key, it, visitor_factory)
            if next_visitor:
                visitor.add_child(next_key, next_visitor)

            if skipped:
                # Make the next value we visit the one we skipped. This will
                # bubble up the stack until we either find the root node that handles
                # it, or we're done
                next_val.push_next(skipped[0], skipped[1])


        else:
            # Base case -- no children
            visitor.visit(next_key, next_val.value())


    skipped_val = None

    if next_val.key() and not next_val.key().startswith(key):
        # we exited because we've passed this level of iteration. Pass that back up
        skipped_val = (next_val.key().encode(), next_val.value())

    if next_val.first_found_key() and next_val.first_found_key().startswith(key):
        return visitor, skipped_val
    else:
        return None, None

class Wrapper:
    def __init__(self, iter):
        self.iter = iter
        self.cur_item = None
        self.first_key = None
        self.forced = None

    def first_found_key(self):
        return self.first_key

    def push_next(self, key, value):
        self.forced = (key, value)

    def next(self):
        if self.forced:
            self.cur_item = self.forced
            self.forced = None
        else:
            next_item = next(self.iter, None)

            # some iterators just return keys. Handle that here
            if next_item is not None and not isinstance(next_item, tuple):
                self.cur_item = (next_item, None)
            else:
                self.cur_item = next_item

        if not self.first_key and self.cur_item:
            self.first_key = self.key()

        return self.cur_item

    def key(self):
        if not self.cur_item:
            return None
        return self.cur_item[0].decode("utf-8")

    def value(self):
        if not self.cur_item:
            return None
        else:
            return self.cur_item[1]
