import json
import pytest

from rocks_quarry.http_handlers import get_handler
from rocks_quarry.http_handlers.tests import fake_db

@pytest.fixture
def create_tester():
    db = fake_db.FakeFB()
    handler = get_handler.GetHandler(db)
    return (handler, db)

_ITEMS= [
    ("abc", "def"),
    ("123", "foo"),
    ("cool", "thing")
]

@pytest.fixture(params = _ITEMS)
def get_items(request):
    return request.param

def test_get_scalar_value(create_tester, get_items):
    handler, db = create_tester
    key = get_items[0].encode()
    value = get_items[1].encode()
    db.put(key, value)
    status, result = handler.handle_request(key)

    assert status == 200
    assert result == value

def test_get_child_value(create_tester):
    handler, db = create_tester
    db.put(b'root/', b'empty')
    db.put(b'root/blah', b'some_item')

    status, result = handler.handle_request(b"root/")
    assert status == 200

    result_from_json = json.loads(result)
    assert result_from_json == {"root" : {"blah" : "some_item"}}

def test_get_child_value_stuff_before(create_tester):
    handler, db = create_tester
    db.put(b'ro/', b'empty')
    db.put(b'rot/', b'empty')
    db.put(b'root/', b'empty')
    db.put(b'root/blah', b'some_item')

    status, result = handler.handle_request(b"root/")
    assert status == 200

    result_from_json = json.loads(result)
    assert result_from_json == {"root" : {"blah" : "some_item"}}

def test_get_many_children_with_overlap(create_tester):
    handler, db = create_tester
    db.put(b"root/", b"")
    db.put(b"root/o", b"o")
    db.put(b"root/o/", b"o/")
    db.put(b"root/o/o", b"o/o")
    db.put(b"root/oo",  b"oo")
    db.put(b"root/oo/", b"oo/")
    db.put(b"root/oo/o", b"oo/o")
    db.put(b"root/oo/ob", b"oo/ob")
    db.put(b"roots", b"")
    db.put(b"roots/", b"")
    db.put(b"roots/o", b"roots/o")
    status, result = handler.handle_request(b"root/")
    assert status == 200

    result_from_json = json.loads(result)
    assert result_from_json == {
        "root": {
            "o" : {
                "o" : "o/o"
            },
            "oo" : {
                "o" : "oo/o",
                "ob" : "oo/ob"
            }
        }
    }
