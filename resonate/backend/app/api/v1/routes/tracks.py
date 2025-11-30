from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.track import Track
from app.schemas.track import TrackOut

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("", response_model=list[TrackOut])
def list_tracks(
    q: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Track)
    if q:
        query = query.filter(Track.title.ilike(f"%{q}%"))
    tracks = query.offset(offset).limit(limit).all()
    return [
        TrackOut(
            id=t.id,
            title=t.title,
            duration_ms=t.duration_ms,
            explicit=t.explicit,
            stream_url=t.audio_url,
        )
        for t in tracks
    ]


@router.get("/{track_id}", response_model=TrackOut)
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Track not found",
        )
    return TrackOut(
        id=track.id,
        title=track.title,
        duration_ms=track.duration_ms,
        explicit=track.explicit,
        stream_url=track.audio_url,
    )
