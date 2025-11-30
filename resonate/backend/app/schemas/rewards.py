from pydantic import BaseModel
from datetime import datetime


class TokenTransactionOut(BaseModel):
    id: int
    delta_btn: int
    type: str
    source: str | None
    created_at: datetime

    class Config:
        orm_mode = True


class TokenBalanceOut(BaseModel):
    balance_btn: int
    recent_transactions: list[TokenTransactionOut]
