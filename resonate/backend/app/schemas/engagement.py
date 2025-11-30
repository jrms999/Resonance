from pydantic import BaseModel


class PlayCompleteIn(BaseModel):
    track_id: int
    duration_ms: int
    device_type: str | None = None


class PlayEventOut(BaseModel):
    play_event_id: int
    granted_btn: int
