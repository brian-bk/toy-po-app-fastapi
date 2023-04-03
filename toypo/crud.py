"""CRUD (Create, Read, Update, Delete) operations

Our CRUD module manages how operations to objects
in our database should be handled. SQL models
will be validated here.

Application-specific logic does not happen at this level,
i.e., creating a PO tracks it in the database and calls
out to item inventory. Such an application operation
is managed above the CRUD module -- this CRUD module
would only handle the DB creating the PO in that example.
"""
from sqlalchemy.orm import Session

from . import models, schemas


def get_purchase_order(db: Session, purchase_order_id: int):
    """Get a single purchase order

    Args:
        db (Session): database
        purchase_order_id (int): PO ID

    Returns:
        models.PurchaseOrder | None: PO if it exists
    """

    return db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.id == purchase_order_id
    ).first()


def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100):
    """Get several purchase orders

    Args:
        db (Session): database
        skip (int, optional): Start page at skip. Defaults to 0.
        limit (int, optional): Max list size. Defaults to 100.

    Returns:
        list[models.PurchaseOrder]: _description_
    """

    return db.query(models.PurchaseOrder).offset(skip).limit(limit).all()


def create_purchase_order(db: Session, purchase_order: schemas.PurchaseOrderCreate):
    """Create a PO

    If the PO we want to create is associated with a PA, we
    do validation from the PO <=> PA here.

    Args:
        db (Session): database
        purchase_order (schemas.PurchaseOrderCreate): New PO data

    Raises:
        ValueError: If PA does not match PO (only if there is a PA)

    Returns:
        models.PurchaseOrder: PO created from db
    """

    db_purchase_order = models.PurchaseOrder(
        **vars(purchase_order)
    )
    db.add(db_purchase_order)

    db.flush()

    if db_purchase_order.purchase_agreement is not None:
        for check_field in ['seller_id', 'buyer_id', 'item_id']:
            if getattr(db_purchase_order.purchase_agreement, check_field) != \
                    getattr(purchase_order, check_field):
                raise ValueError(
                    f'{check_field} must match one in the Purchase Agreement')

    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order


def update_purchase_order(db: Session, purchase_order: schemas.PurchaseOrderUpdate):
    """Update a PO

    If no PO exists, we return None

    Args:
        db (Session): database
        purchase_order (schemas.PurchaseOrderUpdate): PO update fields
            Fields that are None are not updated.

    Returns:
        models.PurchaseOrder | None: Update DB PO
    """

    db_purchase_order = db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.id == purchase_order.id).first()
    if db_purchase_order is None:
        return None

    # Update model class variable from requested fields
    for var, value in vars(purchase_order).items():
        if value is not None:
            setattr(db_purchase_order, var, value)

    db.commit()
    db.refresh(db_purchase_order)
    return db_purchase_order


def get_purchase_agreement(db: Session, purchase_agreement_id: int):
    """Get a PA

    Args:
        db (Session): database
        purchase_agreement_id (int): PA ID

    Returns:
        models.PurchaseAgreement | None: _description_
    """

    return db.query(models.PurchaseAgreement).filter(
        models.PurchaseAgreement.id == purchase_agreement_id
    ).first()


def get_purchase_agreements(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of PAs

    Args:
        db (Session): database
        skip (int, optional): Start at. Defaults to 0.
        limit (int, optional): Page size limit. Defaults to 100.

    Returns:
        list[models.PurchaseAgreement]: _description_
    """
    return db.query(models.PurchaseAgreement).offset(skip).limit(limit).all()


def create_purchase_agreement(db: Session, purchase_agreement: schemas.PurchaseAgreementCreate):
    """Create a PA

    Args:
        db (Session): database
        purchase_agreement (_.PurchaseAgreementCreate): PA create data

    Returns:
        models.PurchaseAgreement: PA created in DB
    """

    db_purchase_agreement = models.PurchaseAgreement(
        **vars(purchase_agreement)
    )
    db.add(db_purchase_agreement)
    db.commit()
    db.refresh(db_purchase_agreement)
    return db_purchase_agreement
