# pylint: disable=not-callable
import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class PurchaseOrderStatus(enum.StrEnum):
    purchased = 'PURCHASED'
    received = 'RECEIVED'
    delivered = 'DELIVERED'


class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(String, index=True, comment='Seller User ID, external')
    buyer_id = Column(String, index=True, comment='Buyer User ID, external')
    item_id = Column(String, index=True, comment='Item ID')
    item_quantity = Column(Integer, comment='Number of items')
    status = Column(Enum(PurchaseOrderStatus),
                    default=PurchaseOrderStatus.purchased, comment='Status of the PO.')
    purchase_agreement_id = Column(Integer, ForeignKey('purchase_agreements.id'),
                                   nullable=True, comment='Associated purchase agreement, if it exists.')
    price_usd = Column(
        Float, comment='Price in USD as floating point number')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # I would be interested in adding an updated_at field but sqlite doesn't
    # support OOTB. I think it'd be better to ignore while it's not a requirement
    # because any real app wouldn't be using sqlite anyways.

    purchase_agreement = relationship(
        'PurchaseAgreement', back_populates='purchase_orders')


class PurchaseAgreement(Base):
    __tablename__ = 'purchase_agreements'

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(String, index=True, comment='Seller User ID, external')
    buyer_id = Column(String, index=True, comment='Buyer User ID, external')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    item_id = Column(String, index=True, comment='Item ID for the PA')
    item_quantity = Column(
        Integer, comment='Number of items for the entire PA')
    price_usd = Column(
        Float, comment='Total price in USD as floating point number')

    purchase_orders = relationship(
        'PurchaseOrder', back_populates='purchase_agreement')
