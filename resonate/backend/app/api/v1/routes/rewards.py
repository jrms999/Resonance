from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.token import TokenBalance, TokenTransaction
from app.schemas.rewards import TokenBalanceOut, TokenTransactionOut
from app.models.user import User

router = APIRouter(prefix="/me/tokens", tags=["rewards"])


@router.get("", response_model=TokenBalanceOut)
def get_my_tokens(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    balance = (
        db.query(TokenBalance)
        .filter(TokenBalance.user_id == current_user.id)
        .first()
    )
    if not balance:
        balance = TokenBalance(user_id=current_user.id, balance_btn=0)
        db.add(balance)
        db.commit()
        db.refresh(balance)

    txs = (
        db.query(TokenTransaction)
        .filter(TokenTransaction.user_id == current_user.id)
        .order_by(TokenTransaction.created_at.desc())
        .limit(20)
        .all()
    )
    return TokenBalanceOut(
        balance_btn=balance.balance_btn,
        recent_transactions=txs,
    )
