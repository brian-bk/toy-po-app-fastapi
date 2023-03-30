from datetime import datetime
from typing import Optional
from pydantic import BaseModel, PositiveInt


class PurchaseOrderBase(BaseModel):
    seller_id: str
    buyer_id: str
    price_usd: float


class PurchaseOrderCreate(PurchaseOrderBase):
    purchase_agreement_id: Optional[int] = None


class PurchaseOrder(PurchaseOrderBase):
    id: PositiveInt
    purchase_agreement_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

class PurchaseAgreementBase(BaseModel):
    seller_id: str
    buyer_id: str


class PurchaseAgreementCreate(PurchaseAgreementBase):
    pass


class PurchaseAgreement(PurchaseAgreementBase):
    id: PositiveInt
    purchase_orders: list[PurchaseOrder] = []
    created_at: datetime

    class Config:
        orm_mode = True
