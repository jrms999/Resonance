from pydantic import BaseModel


class TrackOut(BaseModel):
    id: int
    title: str
    duration_ms: int
    explicit: bool
    stream_url: str

    class Config:
        orm_mode = True
