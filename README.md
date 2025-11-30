# Resonance
Music streaming service


Resonate 🎧

A music streaming app with Bitcoin-flavoured engagement rewards (BTN tokens).

Resonate is a Spotify-style streaming backend + starter mobile client where:

Users stream tracks and earn BTN (BeatCoin) loyalty tokens for engagement.

BTN can be used for rewards (e.g. premium time, perks) and supporting artists.

Audio is stored in S3 and streamed via presigned URLs.

Artists can upload tracks directly to S3 via presigned PUT URLs.

This repo currently focuses on the backend API (FastAPI) and a React Native (Expo) client skeleton.

Features (MVP)

Backend

User registration & login (JWT auth)

Roles: user, artist, admin

Music catalog: artists, albums, tracks

Engagement:

Log plays (play-complete)

Like tracks

Rewards:

BTN balances per user

Auto-earning BTN on:

Full/partial plays

First likes

Daily earning cap

Artist portal APIs:

Generate presigned upload URLs (S3 PUT)

Create tracks linked to artist profiles

Admin endpoints:

/admin/health

/admin/stats (users, tracks, plays, BTN issued)

Mobile client (Expo)

Register / login

List tracks

“Play” a track (calls play-complete, earns BTN)

View token balance + recent transactions

Tech Stack

Backend

Python 3.11+

FastAPI

SQLAlchemy 2.x + Alembic

PostgreSQL

JWT auth (python-jose)

Password hashing (passlib[bcrypt])

AWS S3 (boto3) for audio storage, presigned GET/PUT

Mobile

React Native (Expo, TypeScript)

Axios for API calls

Architecture (high-level)

Modular monolith backend with modules:

auth, users, catalog/tracks, playlists, engagement, rewards, subscriptions (stub), artist, admin

PostgreSQL schema includes:

users, artists, albums, tracks

play_events, user_tracks

token_balances, token_transactions

user_artists (user↔artist mapping)

S3 storage:

storage_key for audio objects (artists/{artist_id}/{uuid}_{filename})

Presigned GET URLs returned as stream_url

Presigned PUT URLs for artist uploads

Prerequisites

Docker + docker-compose or:

Python 3.11+

PostgreSQL

Node.js + npm/yarn (for the mobile app)

AWS account + S3 bucket (for real audio streaming)
