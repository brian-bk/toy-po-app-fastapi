
from threading import Lock
from typing import TypedDict
from contextlib import contextmanager


class ItemStorage(TypedDict):
    available: int
    purchased: int
    received: int
    delivered: int


class ItemNotFound(Exception):
    pass


class NotEnoughItem(Exception):
    pass


class ExampleItemInventory:

    def __init__(self) -> None:
        self._init_example_storage()

    def _init_example_storage(self):
        self.items: dict[str, ItemStorage] = {
            'item1': {
                'available': 100,
                'purchased': 0,
                'received': 0,
                'delivered': 0
            },
            'item2': {
                'available': 100,
                'purchased': 0,
                'received': 0,
                'delivered': 0
            },
            'item3': {
                'available': 1,
                'purchased': 0,
                'received': 0,
                'delivered': 0
            },
            'item4': {
                'available': 0,
                'purchased': 0,
                'received': 0,
                'delivered': 0
            }
        }
        self.lock = Lock()

    def _sub_quantity(self, item_id: str, storage_key: str, quantity: int):
        item = self.items.get(item_id)
        if item is None:
            raise ItemNotFound(f"Item '{item_id}' was not found")
        with self.lock:
            new_quantity = item[storage_key] - quantity
            if new_quantity < 0:
                raise NotEnoughItem(f"Not enough '{item_id}' in {storage_key}")
            item[storage_key] = new_quantity
        return item

    def _add_quantity(self, item_id: str, storage_key: str, quantity: int):
        item = self.items.get(item_id)
        if item is None:
            raise ItemNotFound(f"Item '{item_id}' was not found")
        with self.lock:
            item[storage_key] += quantity
        return item

    def check_item(self, item_id: str):
        item = self.items.get(item_id)
        if item is None:
            raise ItemNotFound(f"Item '{item_id}' was not found")

    @contextmanager
    def transact_item_storage(self, item_id: str, source_storage_key: str, target_storage_key: str, quantity: int):
        self._sub_quantity(item_id, source_storage_key, quantity)
        try:
            yield
        except Exception as e:
            self._add_quantity(item_id, source_storage_key, quantity)
            raise e
        self._add_quantity(item_id, target_storage_key, quantity)


item_inventory = ExampleItemInventory()
