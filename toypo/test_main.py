"""Tests on general FastAPI application
"""
from fastapi.testclient import TestClient

from .inventory import item_inventory
from .main import app

client = TestClient(app)


def test_create_basic_purchase_order_and_receive_it():
    """Create a basic PO and receive it

    Basically the most basic "happy" path.

    We also check that inventory is utilized.
    """
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0
    assert item_inventory.check_item('item1')['received'] == 0
    initial_state = client.get("/purchase_orders/")
    assert initial_state.status_code == 200
    assert initial_state.json() == []

    new_po_response = client.post('/purchase_orders', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'item_id': 'item1',
        'item_quantity': 3,
        'price_usd': 350.5,
    })
    assert new_po_response.status_code == 200
    assert new_po_response.json()['id'] == 1
    assert new_po_response.json()['status'] == 'PURCHASED'
    assert item_inventory.check_item('item1')['available'] == 97
    assert item_inventory.check_item('item1')['purchased'] == 3
    assert item_inventory.check_item('item1')['received'] == 0

    rec_po_response = client.post('/purchase_orders/receive/1')
    assert rec_po_response.status_code == 200
    assert rec_po_response.json()['id'] == 1
    assert rec_po_response.json()['status'] == 'RECEIVED'
    assert item_inventory.check_item('item1')['available'] == 97
    assert item_inventory.check_item('item1')['purchased'] == 0
    assert item_inventory.check_item('item1')['received'] == 3


def test_create_po_too_many_items():
    """Create a PO with more items that are in the
    ExampleItemInventory should fail.

    Then check that the inventory has not changed.
    """
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0
    new_po_response = client.post('/purchase_orders', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'item_id': 'item1',
        'item_quantity': 9001,
        'price_usd': 350.5,
    })
    assert new_po_response.status_code == 400
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0


def test_create_po_no_pa():
    """Create a PO without a matched up PA should fail
    """
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0
    new_po_response = client.post('/purchase_orders', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'item_id': 'item1',
        'item_quantity': 9,
        'price_usd': 350.5,
        'purchase_agreement_id': 387
    })
    assert new_po_response.status_code == 400
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0


def test_create_pa_and_po():
    """Create a PO with a matched up PA.
    """
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0
    new_pa_response = client.post('/purchase_agreements', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'item_id': 'item1',
        'item_quantity': 9,
        'price_usd': 350.5,
    })
    assert new_pa_response.status_code == 200
    assert new_pa_response.json()['id'] == 1
    assert item_inventory.check_item('item1')['available'] == 100
    assert item_inventory.check_item('item1')['purchased'] == 0

    new_po_response = client.post('/purchase_orders', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'item_id': 'item1',
        'item_quantity': 9,
        'price_usd': 350.5,
        'purchase_agreement_id': 1
    })
    assert new_po_response.status_code == 200
    assert new_po_response.json()['id'] == 1
    assert new_po_response.json()['purchase_agreement_id'] == 1
    assert item_inventory.check_item('item1')['available'] == 91
    assert item_inventory.check_item('item1')['purchased'] == 9
