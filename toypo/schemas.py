from datetime import datetime
from typing import Optional
# pylint: disable=no-name-in-module,no-self-argument
from pydantic import BaseModel, PositiveInt

from .models import PurchaseOrderStatus


class PurchaseOrderBase(BaseModel):
    pass


class PurchaseOrderCreate(PurchaseOrderBase):
    seller_id: str
    buyer_id: str
    item_id: str
    item_quantity: int
    price_usd: float
    purchase_agreement_id: Optional[int] = None


class PurchaseOrderUpdate(PurchaseOrderBase):
    id: PositiveInt
    status: Optional[PurchaseOrderStatus] = None


class PurchaseOrder(PurchaseOrderBase):
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
    seller_id: str
    buyer_id: str
    item_id: str
    item_quantity: int
    price_usd: float


class PurchaseAgreementCreate(PurchaseAgreementBase):
    pass


class PurchaseAgreement(PurchaseAgreementBase):
    id: PositiveInt
    purchase_orders: list[PurchaseOrder] = []
    created_at: datetime

    class Config:
        orm_mode = True
