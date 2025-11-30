from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.token import TokenBalance, TokenTransaction
from app.models.play_event import PlayEvent
from app.models.user import User
from app.models.track import Track

DAILY_EARN_CAP_BTN = 100
BTN_FULL_PLAY = 2
BTN_PARTIAL_PLAY = 1


def _today_earned(db: Session, user_id: int) -> int:
    today = date.today()
    start = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)
    total = (
        db.query(func.coalesce(func.sum(TokenTransaction.delta_btn), 0))
        .filter(
            TokenTransaction.user_id == user_id,
            TokenTransaction.type == "earn",
            TokenTransaction.created_at >= start,
        )
        .scalar()
    )
    return int(total or 0)


def _apply_earn(db: Session, user_id: int, delta_btn: int, source: str, metadata: dict | None = None) -> int:
    if delta_btn <= 0:
        return 0
    earned = _today_earned(db, user_id)
    remaining = max(DAILY_EARN_CAP_BTN - earned, 0)
    if remaining <= 0:
        return 0
    grant = min(delta_btn, remaining)

    balance = db.query(TokenBalance).filter(TokenBalance.user_id == user_id).first()
    if not balance:
        balance = TokenBalance(user_id=user_id, balance_btn=0)
        db.add(balance)
        db.flush()

    balance.balance_btn += grant
    tx = TokenTransaction(
        user_id=user_id,
        delta_btn=grant,
        type="earn",
        source=source,
        metadata=metadata or {},
    )
    db.add(tx)
    return grant


def award_for_play_complete(db: Session, user: User, track: Track, play_event: PlayEvent) -> int:
    if play_event.full_play:
        delta = BTN_FULL_PLAY
    else:
        if not play_event.duration_ms or play_event.duration_ms < 30_000:
            return 0
        delta = BTN_PARTIAL_PLAY
    return _apply_earn(
        db=db,
        user_id=user.id,
        delta_btn=delta,
        source="play_complete",
        metadata={"track_id": track.id, "play_event_id": play_event.id},
    )
