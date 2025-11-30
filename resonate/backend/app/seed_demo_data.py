from app.core.database import SessionLocal
from app.models.track import Track


def seed():
    db = SessionLocal()
    try:
        if db.query(Track).count() > 0:
            print("Seed: tracks already exist, skipping.")
            return
        t1 = Track(
            title="Midnight Drive",
            duration_ms=198000,
            audio_url="https://example.com/audio/midnight-drive.mp3",
            explicit=False,
        )
        t2 = Track(
            title="Neon Skies",
            duration_ms=215000,
            audio_url="https://example.com/audio/neon-skies.mp3",
            explicit=False,
        )
        db.add_all([t1, t2])
        db.commit()
        print("Seed: demo tracks inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
