import json
import pytest

from rocks_quarry.http_handlers import delete_handler
from rocks_quarry.http_handlers.tests import fake_db

@pytest.fixture
def create_tester():
    db = fake_db.FakeFB()
    handler = delete_handler.DeleteHandler(db)
    return (handler, db)

def test_empty(create_tester):
    handler, _ = create_tester

    status, result = handler.handle_request('yo')

    assert status == 404
    assert result == b'Key not found'

def test_no_match(create_tester):
    handler, db = create_tester

    db.put(b"Hello", "world")
    db.put(b"Hello/", "foo")

    status, result = handler.handle_request('yo')

    assert status == 404
    assert result == b'Key not found'

def test_match_single(create_tester):
    handler, db = create_tester

    db.put(b"Hello", "world")
    db.put(b"Hello/", "foo")

    status, result = handler.handle_request(b'Hello')

    assert status == 200
    assert json.loads(result) == {"total" : 1, "deleted" : ["Hello"]}

    # Make sure we deleted what matters
    assert not db.get(b"Hello")
    assert db.get(b"Hello/") == "foo"

def test_match_many(create_tester):
    handler, db = create_tester

    db.put(b"Hello", "world")
    db.put(b"Hello/", "foo")
    db.put(b"Hello/blah", "fip")
    db.put(b"Hello/bar", "qux")

    status, result = handler.handle_request(b'Hello/')

    assert status == 200
    assert json.loads(result) == {"total" : 3, "deleted" : ["Hello/", "Hello/bar", "Hello/blah"]}
    assert not db.get(b"Hello/")
    assert not db.get(b"Hello/bar")
    assert not db.get(b"Hello/blah")
    assert db.get(b"Hello") == "world"

