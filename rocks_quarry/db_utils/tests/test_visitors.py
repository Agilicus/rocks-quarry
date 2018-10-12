from rocks_quarry.db_utils import visitors
from rocks_quarry.db_utils.tests import fake_iterator

class FakeVisitor:
    def __init__(self):
        self.containers = set()
        self.leafs = dict()

    def add_child(self, full_name, child):
        self.containers.update(child.containers)
        self.leafs.update(child.leafs)

    def visit(self, full_name, next_value):
        self.leafs[full_name] = next_value

    def visit_container(self, full_name, value):
        self.containers.add(full_name)

def factory():
    return FakeVisitor()

def test_empty_children():
    it = fake_iterator.build_fake_iterator({})

    result = visitors.children_visitor("", it, factory)

    assert not result

def test_no_match():
    it = fake_iterator.build_fake_iterator({b"abc" : b"hello", b"foo" : b"bar"})

    result = visitors.children_visitor("blah", it, factory)

    assert not result

def test_overlap_no_children():
    it = fake_iterator.build_fake_iterator({b"abc/" : b"hello", b"foo" : b"bar"})

    result = visitors.children_visitor("ab", it, factory)

    assert not result

def test_overlap_with_children():
    input_dict = {
        b"root/" : "",
        b"root/o" : "o",
        b"root/o/" : "o/",
        b"root/o/o" : "o/o",
        b"root/oo" :  "oo",
        b"root/oo/" : "oo/",
        b"root/oo/o" : "oo/o"
    }
    it = fake_iterator.build_fake_iterator(input_dict)
    result = visitors.children_visitor("root/", it, factory)
    assert result

    assert result.containers == set(["root/", "root/o/", "root/oo/"])
    assert result.leafs == {"root/o" : "o", "root/o/o" : "o/o", "root/oo" : "oo", "root/oo/o" : "oo/o"}

def test_overlap_with_children_and_some_outside():
    input_dict = {
        b"root/" : "",
        b"root/o" : "o",
        b"root/o/" : "o/",
        b"root/o/o" : "o/o",
        b"root/oo" :  "oo",
        b"root/oo/" : "oo/",
        b"root/oo/o" : "oo/o",
        b"roots" : "",
        b"roots/" : "",
        b"roots/o" : "roots/o"
    }
    it = fake_iterator.build_fake_iterator(input_dict)
    result = visitors.children_visitor("root/", it, factory)
    assert result

    assert result.containers == set(["root/", "root/o/", "root/oo/"])
    assert result.leafs == {"root/o" : "o", "root/o/o" : "o/o", "root/oo" : "oo", "root/oo/o" : "oo/o"}

def test_single_node():
    input_dict = {
        b"root/" : "",
    }
    it = fake_iterator.build_fake_iterator(input_dict)
    result = visitors.children_visitor("root/", it, factory)
    assert result

    assert result.containers == set(["root/"])
    assert result.leafs == {}

def test_no_item_iterator():
    it = iter([b"root/", b"root/o"])

    result = visitors.children_visitor("root/", it, factory)
    assert(result)

    assert result.containers == set(["root/"])
    assert result.leafs["root/o"] == None
