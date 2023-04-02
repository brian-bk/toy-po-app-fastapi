from logging import getLogger

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import constants, crud, inventory, models, schemas
from .database import SessionLocal, engine

logger = getLogger(__name__)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except (IntegrityError, ValueError) as bad_input:
        raise HTTPException(400, detail=str(bad_input)) from bad_input
    finally:
        db.close()


def get_item_inventory():
    try:
        yield inventory.item_inventory
    except inventory.ItemNotFound as not_found:
        raise HTTPException(404, detail=str(not_found)) from not_found
    except inventory.NotEnoughItem as bad_input:
        raise HTTPException(400, detail=str(bad_input)) from bad_input


def auto_migrate():
    logger.info('Running auto migrations')
    # @todo would use a real migration tool like
    # alembic, this only works well from an empty
    # database.
    models.Base.metadata.create_all(bind=engine)


@app.get('/purchase_orders/', response_model=list[schemas.PurchaseOrder])
def read_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchase_orders = crud.get_purchase_orders(db, skip=skip, limit=limit)
    return purchase_orders


@app.get('/purchase_orders/{purchase_order_id}', response_model=schemas.PurchaseOrder)
def read_purchase_order(purchase_order_id, db: Session = Depends(get_db)):
    db_purchase_order = crud.get_purchase_order(
        db, purchase_order_id=purchase_order_id)
    if db_purchase_order is None:
        raise HTTPException(status_code=404, detail='Purchase Order not found')
    return db_purchase_order


@app.post('/purchase_orders/receive/{purchase_order_id}', response_model=schemas.PurchaseOrder)
def receive_purchase_order(purchase_order_id: int, db: Session = Depends(get_db), item_inventory: inventory.ExampleItemInventory = Depends(get_item_inventory)):
    purchase_order_update = schemas.PurchaseOrderUpdate(
        id=purchase_order_id,
        status=models.PurchaseOrderStatus.received,
    )
    db_purchase_order = crud.get_purchase_order(
        db, purchase_order_id=purchase_order_id)
    if db_purchase_order is None:
        raise HTTPException(status_code=404, detail='Purchase Order not found')

    if db_purchase_order.status != models.PurchaseOrderStatus.purchased:
        raise HTTPException(
            status_code=400, detail='Can only receive a PO from purchased status')

    item_id: str = db_purchase_order.item_id  # type: ignore
    item_quantity: int = db_purchase_order.item_quantity  # type: ignore
    with item_inventory.transact_item_storage(item_id, 'purchased', 'received', item_quantity):
        crud.update_purchase_order(
            db, purchase_order=purchase_order_update)
    db.flush()
    return db_purchase_order


@app.post('/purchase_orders/', response_model=schemas.PurchaseOrder)
def create_purchase_order(
    purchase_order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db), item_inventory: inventory.ExampleItemInventory = Depends(get_item_inventory)
):
    with item_inventory.transact_item_storage(purchase_order.item_id, 'available', 'purchased', purchase_order.item_quantity):
        db_purchase_order = crud.create_purchase_order(
            db=db, purchase_order=purchase_order)
    return db_purchase_order


@app.get('/purchase_agreements/{purchase_agreement_id}', response_model=schemas.PurchaseAgreement)
def read_purchase_purchase_agreement(purchase_agreement_id, db: Session = Depends(get_db)):
    db_purchase_agreement = crud.get_purchase_agreement(
        db, purchase_agreement_id=purchase_agreement_id)
    if db_purchase_agreement is None:
        raise HTTPException(
            status_code=404, detail='Purchase Agreement not found')
    return db_purchase_agreement


@app.get('/purchase_agreements/', response_model=list[schemas.PurchaseAgreement])
def read_purchase_agreements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchase_agreements = crud.get_purchase_agreements(
        db, skip=skip, limit=limit)
    return purchase_agreements


@app.post('/purchase_agreements/', response_model=schemas.PurchaseAgreement)
def create_purchase_agreement(
    purchase_agreement: schemas.PurchaseAgreementCreate, db: Session = Depends(get_db), item_inventory: inventory.ExampleItemInventory = Depends(get_item_inventory)
):
    item_inventory.check_item(purchase_agreement.item_id)
    return crud.create_purchase_agreement(db=db, purchase_agreement=purchase_agreement)


if constants.AUTO_MIGRATE:
    auto_migrate()
