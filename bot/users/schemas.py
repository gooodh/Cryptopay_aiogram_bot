from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Payload(BaseModel):
    invoice_id: int
    hash: Optional[str] = None
    currency_type: Optional[str] = None
    asset: Optional[str] = None
    amount: Optional[float] = None
    paid_asset: Optional[str] = None
    paid_amount: Optional[str] = None
    fee_asset: Optional[str] = None
    fee_amount: Optional[str] = None
    fee: Optional[str] = None
    fee_in_usd: Optional[str] = None
    pay_url: Optional[str] = None
    bot_invoice_url: Optional[str] = None
    mini_app_invoice_url: Optional[str] = None
    web_app_invoice_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    allow_comments: Optional[bool] = None
    allow_anonymous: Optional[bool] = None
    paid_usd_rate: Optional[str] = None
    usd_rate: Optional[str] = None
    paid_at: Optional[str] = None
    paid_anonymously: Optional[bool] = None
    payload: Optional[str] = None


class Update(BaseModel):
    update_id: int
    update_type: str
    request_date: datetime
    payload: Payload
