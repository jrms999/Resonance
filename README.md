# Resonance

Resonance is an early FastAPI backend prototype for a music-engagement rewards product. It explores awarding **BTN** loyalty points when authenticated users listen to tracks.

## Repository status

This repository currently contains the backend only. It is a prototype, not a production-ready streaming service.

### Implemented

- User registration and JWT-based login
- Track listing and individual track lookup
- Recording play-complete events
- BTN balance and transaction history
- Reward rules:
  - 2 BTN for a full play (at least 80% complete)
  - 1 BTN for a partial play of at least 30 seconds
  - 100 BTN daily earning cap
- PostgreSQL-backed SQLAlchemy models
- Docker and Docker Compose development files

Tracks currently reference a stored `audio_url`. The repository does not upload, host, or transcode audio.

### Not yet implemented

- React Native or Expo client
- S3 uploads or presigned streaming URLs
- Artist upload portal
- Likes, playlists, subscriptions, or admin dashboards
- Production deployment, monitoring, or a demonstrated migration workflow
- Automated tests

## Important limitations

- Play events do not yet have idempotency or duplicate-play protection. Repeated valid requests can award points until the daily cap is reached.
- Authentication and reward abuse controls need a security review before real users or payments are introduced.
- Docker Compose contains development-only example credentials. Replace all secrets outside local development.
- Dependency compatibility and a clean-start database workflow still need to be locked down and tested.

## Current structure

```text
resonate/
├── api/          # FastAPI routes
├── core/         # configuration and security helpers
├── db/           # SQLAlchemy base and session
├── models/       # users, tracks, play events, token ledger
├── schemas/      # request and response models
└── services/     # reward calculations
```

## Recommended next milestones

1. Add a reproducible local setup with `.env.example`, pinned dependencies, and migrations.
2. Add API tests for authentication, reward thresholds, daily caps, and duplicate requests.
3. Add idempotency and anti-abuse controls to play rewards.
4. Add CI for tests and dependency/security scanning.
5. Build a minimal client only after the backend contract is tested.
6. Add object storage and signed URLs when real audio ingestion is in scope.

The earlier README described several planned features as complete. This version deliberately separates implemented code from roadmap items so the portfolio accurately reflects the repository.
