from logging import getLogger

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import constants, crud, models, schemas
from .database import SessionLocal, engine

logger = getLogger(__name__)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except IntegrityError as ie:
        logger.warning(
            "IntegrityError caught, response will be 400", exc_info=True)
        raise HTTPException(400, detail=str(ie)) from ie
    finally:
        db.close()


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
def read_purchase_orders(purchase_order_id, db: Session = Depends(get_db)):
    db_purchase_order = crud.get_purchase_order(
        db, purchase_order_id=purchase_order_id)
    if db_purchase_order is None:
        raise HTTPException(status_code=404, detail='Purchase Order not found')
    return db_purchase_order


@app.post('/purchase_orders/receive/{purchase_order_id}', response_model=schemas.PurchaseOrder)
def receive_purchase_order(purchase_order_id: int, db: Session = Depends(get_db)):
    purchase_order_update = schemas.PurchaseOrderUpdate(
        id=purchase_order_id,
        status=models.PurchaseOrderStatus.received,
    )
    purchase_order = crud.update_purchase_order(
        db, purchase_order=purchase_order_update)
    return purchase_order


@app.post('/purchase_orders/', response_model=schemas.PurchaseOrder)
def create_purchase_order(
    purchase_order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)
):
    try:
        return crud.create_purchase_order(db=db, purchase_order=purchase_order)
    except ValueError as ve:
        raise HTTPException(400, detail=str(ve)) from ve


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
    purchase_agreement: schemas.PurchaseAgreementCreate, db: Session = Depends(get_db)
):
    return crud.create_purchase_agreement(db=db, purchase_agreement=purchase_agreement)


if constants.AUTO_MIGRATE:
    auto_migrate()
