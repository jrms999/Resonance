"""Create missing tables for an empty local demo database; not a migration tool."""
from app.models import Base
from app.core.database import engine


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
