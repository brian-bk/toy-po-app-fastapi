import os

import pytest

from toypo.database import SessionLocal
from toypo.inventory import item_inventory
from toypo.main import _auto_migrate

db = SessionLocal()


SQL_ALCHEMY_URL = os.environ['SQL_ALCHEMY_URL']
if 'test' not in SQL_ALCHEMY_URL:
    raise Exception(
        f"""SQL_ALCHEMY_URL does not contain "test", is this a test db url?
        It was {SQL_ALCHEMY_URL}""")


@pytest.fixture(autouse=True)
def clean_db():
    """Clean DB between tests

    This is rather inefficient for a lot of tests but
    fine for now.

    It would be better to just remove data/tables,
    or roll back each transaction between tests.
    """
    _auto_migrate()
    yield
    os.remove(db.connection().engine.url.translate_connect_args()['database'])


@pytest.fixture(autouse=True)
def clean_inventory():
    """Clean Item Inventory between tests
    """
    item_inventory._init_example_storage()
    yield
