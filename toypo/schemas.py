from typing import Optional
from pydantic import BaseModel, PositiveInt


class PurchaseOrderBase(BaseModel):
    pass


class PurchaseOrderCreate(PurchaseOrderBase):
    purchase_agreement_id: Optional[int] = None


class PurchaseOrder(PurchaseOrderBase):
    id: PositiveInt

    class Config:
        orm_mode = True

class PurchaseAgreementBase(BaseModel):
    pass


class PurchaseAgreementCreate(PurchaseAgreementBase):
    pass


class PurchaseAgreement(PurchaseAgreementBase):
    id: PositiveInt
    purchase_orders: list[PurchaseOrder] = []

    class Config:
        orm_mode = True
