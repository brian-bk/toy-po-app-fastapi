"""Pydantic Models

Separate from ORM Models, these models
are closer to the application.

Valid CRUD operations on ORM models are defined here.
"""
# pylint: disable=missing-class-docstring
from datetime import datetime
from typing import Optional
# pylint: disable=no-name-in-module,no-self-argument
from pydantic import BaseModel, PositiveInt

from .models import PurchaseOrderStatus


class PurchaseOrderBase(BaseModel):
    """Base PO Model
    It's empty because create and update models do not
    have much overlap.
    """


class PurchaseOrderCreate(PurchaseOrderBase):
    """PO create operation fields
    """
    seller_id: str
    buyer_id: str
    item_id: str
    item_quantity: int
    price_usd: float
    purchase_agreement_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "seller_id": "seller123",
                'buyer_id': 'buyer321',
                'item_id': 'item2',
                'item_quantity': 99,
                'price_usd': 350,
                'purchase_agreement_id': 1,
            }
        }


class PurchaseOrderUpdate(PurchaseOrderBase):
    """PO update operation fields

    We need the `id` to get the PO in the first place.
    """
    id: PositiveInt
    status: Optional[PurchaseOrderStatus] = None


class PurchaseOrder(PurchaseOrderBase):
    """PO model as returned to the client
    """
    id: PositiveInt
    seller_id: str
    buyer_id: str
    item_id: str
    item_quantity: int
    price_usd: float
    purchase_agreement_id: Optional[int] = None
    status: PurchaseOrderStatus
    created_at: datetime

    class Config:
        orm_mode = True


class PurchaseAgreementBase(BaseModel):
    """Base PA Model

    This has more fields than the base PO model
    because as of now, we cannot update PAs.
    """
    seller_id: str
    buyer_id: str
    item_id: str
    item_quantity: int
    price_usd: float


class PurchaseAgreementCreate(PurchaseAgreementBase):
    """PA create operation fields

    Right now, just matches the base PA model
    """

    class Config:
        schema_extra = {
            "example": {
                "seller_id": "seller123",
                'buyer_id': 'buyer123',
                'item_id': 'item1',
                'item_quantity': 2,
                'price_usd': 3.5,
            }
        }


class PurchaseAgreement(PurchaseAgreementBase):
    """PA model as returned to the client
    """
    id: PositiveInt
    purchase_orders: list[PurchaseOrder] = []
    created_at: datetime

    class Config:
        orm_mode = True
