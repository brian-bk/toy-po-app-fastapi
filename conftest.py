import os

import pytest

from toypo.database import Base, SessionLocal
from toypo.inventory import item_inventory
from toypo.main import _auto_migrate


SQL_ALCHEMY_URL = os.environ['SQL_ALCHEMY_URL']
if 'test' not in SQL_ALCHEMY_URL:
    raise Exception(
        f"""SQL_ALCHEMY_URL does not contain "test", is this a test db url?
        It was {SQL_ALCHEMY_URL}""")


@pytest.fixture(autouse=True)
def clean_db():
    """Clean DB between tests

    Wipe out tables entirely
    """
    db = SessionLocal()
    _auto_migrate()
    yield
    Base.metadata.drop_all(db.connection().engine)


@pytest.fixture(autouse=True, scope='session')
def remove_db():
    """Remove DB at end of session
    """
    db = SessionLocal()
    yield
    os.remove(db.connection().engine.url.translate_connect_args()['database'])


@pytest.fixture(autouse=True)
def clean_inventory():
    """Clean Item Inventory between tests
    """
    item_inventory._init_example_storage()
    yield
