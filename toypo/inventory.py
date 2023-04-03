"""Item Inventory

This isn't a real item inventory, but we create
an example one. It has stubbed item data and
handles item inventory operations.
"""
from threading import Lock
from typing import TypedDict
from contextlib import contextmanager


class ItemStorage(TypedDict):
    """Tracked inventory for a single item
    """
    available: int
    purchased: int
    received: int
    delivered: int


class ItemNotFound(Exception):
    """Item not found

    Should be raised if an item does not exist in the inventory.
    """


class NotEnoughItem(Exception):
    """Not enough items

    Should be raised if there's not enough items to subtract
    from inventory for an inventory operation.
    """


class ExampleItemInventory:
    """An example item inventory

    It has stubbed out contents
    """

    def __init__(self) -> None:
        """Initialize the inventory client
        """
        self._init_example_storage()

    def _init_example_storage(self):
        """Initialize the example inventory client

        Fill it with mock data.
        """
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
        """Subtract quantity from an item storage key

        Args:
            item_id (str): Item ID
            storage_key (str): Where to subtract from (i.e. 'purchased', 'received')
            quantity (int): Quantity to subtract

        Raises:
            ItemNotFound: If item does not exist in inventory
            NotEnoughItem: If there is not enough items in the inventory class
                to subtract.
        """

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
        """Add quantity to an item storage key

        Args:
            item_id (str): Item ID
            storage_key (str): Where to add it to (i.e. 'purchased', 'received')
            quantity (int): Quantity to add

        Raises:
            ItemNotFound: If item does not exist in inventory
        """
        item = self.items.get(item_id)
        if item is None:
            raise ItemNotFound(f"Item '{item_id}' was not found")
        with self.lock:
            item[storage_key] += quantity
        return item

    def check_item(self, item_id: str):
        """Check if item exists

        Args:
            item_id (str): Item ID

        Raises:
            ItemNotFound: Item does not exist in inventory
        """
        item = self.items.get(item_id)
        if item is None:
            raise ItemNotFound(f"Item '{item_id}' was not found")
        return item

    @contextmanager
    def transact_item_storage(
        self,
        item_id: str,
        source_storage_key: str,
        target_storage_key: str,
        quantity: int
    ):
        """A somewhat-safe item storage transaction

        Move an item from source_storage_key to target_storage_key. If an
        exception happens while we're yielding, we try to
        move the quantity back to the source_storage_key.

        @TODO There may be a failure mode where a database record is
        created while this function is yielding, but an exception
        is still raised. In such a case the inventory may not be
        moved over even though a PO claimed it should have.
        In a real multi-services system, it'd be important
        to expect network service failures and such failure modes,
        but it's hard to do a simple design without an overall
        system architecture in place.

        Args:
            item_id (str): Item ID
            source_storage_key (str): Where to move tracked inventory from
            target_storage_key (str): Where to move tracked inventory to
            quantity (int): Quantity to move over

        Raises:
            Exception: Any exception thrown while yielding will be reraised,
            after a cleanup operation.
        """
        self._sub_quantity(item_id, source_storage_key, quantity)
        try:
            yield
        except Exception as e:
            self._add_quantity(item_id, source_storage_key, quantity)
            raise e
        self._add_quantity(item_id, target_storage_key, quantity)


item_inventory = ExampleItemInventory()
