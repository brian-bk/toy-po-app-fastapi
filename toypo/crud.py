from sqlalchemy.orm import Session

from . import models, schemas


def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PurchaseOrder).offset(skip).limit(limit).all()

def create_purchase_order(db: Session, purchase_order: schemas.PurchaseOrderCreate):
    db_purchase_order = models.PurchaseOrder(
        buyer_id=purchase_order.buyer_id,
        seller_id=purchase_order.seller_id,
        price_usd=purchase_order.price_usd,
        purchase_agreement_id=purchase_order.purchase_agreement_id,
    )
    db.add(db_purchase_order)

    db.flush()
    if db_purchase_order.purchase_agreement is not None and \
            db_purchase_order.purchase_agreement.seller_id != purchase_order.seller_id:
        raise ValueError('seller_id must match one in the Purchase Agreement')
    if db_purchase_order.purchase_agreement is not None and \
            db_purchase_order.purchase_agreement.buyer_id != purchase_order.buyer_id:
        raise ValueError('buyer_id must match one in the Purchase Agreement')

    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order

def update_purchase_order(db: Session, purchase_order: schemas.PurchaseOrderUpdate):
    db_purchase_order = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == purchase_order.id).first()
    if db_purchase_order is None:
        return None
    
    # Update model class variable from requested fields 
    for var, value in vars(purchase_order).items():
        if value is not None:
            setattr(db_purchase_order, var, value)

    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order

def get_purchase_agreements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PurchaseAgreement).offset(skip).limit(limit).all()

def create_purchase_agreement(db: Session, purchase_agreement: schemas.PurchaseAgreementCreate):
    db_purchase_agreement = models.PurchaseAgreement(
        buyer_id=purchase_agreement.buyer_id,
        seller_id=purchase_agreement.seller_id,
    )
    db.add(db_purchase_agreement)
    db.commit()
    db.refresh(db_purchase_agreement)
    return db_purchase_agreement
