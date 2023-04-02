from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create_basic_purchase_order_and_receive_it():
    initial_state = client.get("/purchase_orders/")
    assert initial_state.status_code == 200
    assert initial_state.json() == []

    new_po_response = client.post('/purchase_orders', json={
        'seller_id': 'seller123',
        'buyer_id': 'buyer123',
        'price_usd': 350.5,
    })
    assert new_po_response.status_code == 200
    assert new_po_response.json()['id'] == 1
    assert new_po_response.json()['status'] == 'PURCHASED'

    rec_po_response = client.post('/purchase_orders/receive/1')
    assert rec_po_response.status_code == 200
    assert rec_po_response.json()['id'] == 1
    assert rec_po_response.json()['status'] == 'RECEIVED'
