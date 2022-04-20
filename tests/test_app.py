import json
import unittest
from app import app
from db import DB

base = "http://localhost:5000"

class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True 

    def setUp(self):
        DB.create_notes_table_if_not_exists() # FIXME modifies the actual db

    def tearDown(self):
        DB.drop_notes_table_if_exists()

    def test_post(self):
        "test POST /api/notes status is 201"
        response = TestCase.client.post(
            base + "/api/notes",
            json={"content": "hello"},
        )
        self.assertEqual(response.status_code, 201)

    def test_get(self):
        "test GET /api/notes/id"
        response = TestCase.client.post(
            base + "/api/notes",
            json={"content": "hello again"},
        )
        self.assertEqual(response.status_code, 201)
        response = TestCase.client.get(
            base + "/api/notes/1",
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data()),
            {"content": "hello again", "id": 1}
        )

    def test_no_content(self):
        "test GET /api/notes/id when not found"
        response = TestCase.client.get(base + "/api/notes/2")
        self.assertEqual(response.status_code, 404)

