import pytest

from rocks_quarry.http_handlers import put_handler
from rocks_quarry.http_handlers.tests import fake_db

@pytest.fixture
def create_tester():
    db = fake_db.FakeFB()
    handler = put_handler.PutHandler(db)
    return (handler, db)

_ITEMS= [
    ("abc", "def"),
    ("123", "foo"),
    ("cool", "thing")
]

@pytest.fixture(params = _ITEMS)
def get_items(request):
    return request.param

def test_put_is_returned(create_tester, get_items):
    handler, db = create_tester
    key = get_items[0].encode()
    value = get_items[1].encode()

    result = handler.handle_request(key, value)

    assert result == 200
    assert db.get(key) == value
