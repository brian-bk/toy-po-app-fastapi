from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'

    id = Column(Integer, primary_key=True, index=True)
    purchase_agreement_id = Column(Integer, ForeignKey('purchase_agreements.id'),
                                   nullable=True, comment='Associated purchase agreement, if it exists.')

    purchase_agreement = relationship('PurchaseAgreement', back_populates='purchase_orders')

class PurchaseAgreement(Base):
    __tablename__ = 'purchase_agreements'

    id = Column(Integer, primary_key=True, index=True)

    purchase_orders = relationship('PurchaseOrder', back_populates='purchase_agreement')
