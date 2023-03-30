from logging import getLogger

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import constants, crud, models, schemas
from .database import SessionLocal, engine

logger = getLogger(__name__)

if constants.AUTO_MIGRATE:
    logger.info('Running auto migrations')
    # @todo would use a real migration tool like
    # alembic, this only works well from an empty
    # database.
    models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    e = None
    try:
        yield db
    except IntegrityError as ie:
        # @todo log exception with details as warning
        raise HTTPException(status_code=400, detail=str(ie))
    finally:
        db.close()


@app.get('/purchase_orders/', response_model=list[schemas.PurchaseOrder])
def read_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchase_orders = crud.get_purchase_orders(db, skip=skip, limit=limit)
    return purchase_orders

@app.post('/purchase_orders/', response_model=schemas.PurchaseOrder)
def create_purchase_order(
    purchase_order: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)
):
    return crud.create_purchase_order(db=db, purchase_order=purchase_order)

@app.get('/purchase_agreements/', response_model=list[schemas.PurchaseAgreement])
def read_purchase_agreements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchase_agreements = crud.get_purchase_agreements(db, skip=skip, limit=limit)
    return purchase_agreements

@app.post('/purchase_agreements/', response_model=schemas.PurchaseAgreement)
def create_purchase_agreement(
    purchase_agreement: schemas.PurchaseAgreementCreate, db: Session = Depends(get_db)
):
    return crud.create_purchase_agreement(db=db, purchase_agreement=purchase_agreement)
