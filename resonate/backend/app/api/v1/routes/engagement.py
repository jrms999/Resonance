from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.models.track import Track
from app.models.play_event import PlayEvent
from app.schemas.engagement import PlayCompleteIn, PlayEventOut
from app.services.rewards_service import award_for_play_complete

router = APIRouter(prefix="/events", tags=["engagement"])


@router.post("/play-complete", response_model=PlayEventOut)
def play_complete(
    body: PlayCompleteIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    track = db.query(Track).filter(Track.id == body.track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found",
        )

    full_play = body.duration_ms >= int(0.8 * track.duration_ms)

    play_event = PlayEvent(
        user_id=current_user.id,
        track_id=track.id,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        duration_ms=body.duration_ms,
        full_play=full_play,
        device_type=body.device_type,
    )
    db.add(play_event)
    db.flush()

    granted = award_for_play_complete(
        db=db,
        user=current_user,
        track=track,
        play_event=play_event,
    )

    db.commit()
    db.refresh(play_event)

    return PlayEventOut(play_event_id=play_event.id, granted_btn=granted)
