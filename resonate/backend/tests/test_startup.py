"""Local smoke tests; SQLite does not validate PostgreSQL reward concurrency."""
import os
import tempfile
import unittest

_tmp = tempfile.TemporaryDirectory()
os.environ["POSTGRES_DSN"] = "sqlite:///" + _tmp.name + "/demo.db"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-never-use-in-production"

from fastapi.testclient import TestClient
from app.main import app
from app.init_demo_db import main as initialize
from app.seed_demo_data import seed
from app.core.database import Base, engine, SessionLocal
from app.models.token import TokenTransaction


class StartupTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        initialize()
        initialize()  # local bootstrap is safe to repeat
        self.client = TestClient(app)

    def test_startup_and_catalogue(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        seed()
        seed()
        response = self.client.get("/api/v1/tracks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(self.client.get("/api/v1/tracks/999").status_code, 404)

    def test_register_login_and_protected_balance(self):
        credentials = {"email": "demo@example.com", "password": "local-demo-password"}
        self.assertEqual(self.client.get("/api/v1/me/tokens").status_code, 401)
        response = self.client.post("/api/v1/auth/register", json=credentials)
        self.assertEqual(response.status_code, 200, response.text)
        token = response.json()["access_token"]
        balance = self.client.get("/api/v1/me/tokens", headers={"Authorization": "Bearer " + token})
        self.assertEqual(balance.status_code, 200, balance.text)
        self.assertEqual(balance.json()["balance_btn"], 0)
        self.assertEqual(self.client.post("/api/v1/auth/login", json=credentials).status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/register", json=credentials).status_code, 400)
        credentials["password"] = "wrong"
        self.assertEqual(self.client.post("/api/v1/auth/login", json=credentials).status_code, 401)

    def test_transaction_metadata_column_mapping(self):
        with SessionLocal() as db:
            db.add(TokenTransaction(id=1, user_id=1, delta_btn=2, type="earn", details={"track_id": 3}))
            db.commit()
            transaction = db.get(TokenTransaction, 1)
            self.assertEqual(transaction.details, {"track_id": 3})
            self.assertIn("metadata", TokenTransaction.__table__.c)


if __name__ == "__main__":
    unittest.main()
