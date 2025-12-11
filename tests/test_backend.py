import unittest
import os
import json
from app import app
from storage import _save_all, _load_all

class BackendTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # start with known dataset
        sample = {
            "Alpha": {"name":"Alpha","publication_date":"2020-01-01","author":"A","category":"Book"},
            "Beta": {"name":"Beta","publication_date":"2021-05-03","author":"B","category":"Film"}
        }
        _save_all(sample)

    def tearDown(self):
        # clear file
        _save_all({})

    def test_list_all(self):
        r = self.client.get("/media")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(any(x["name"]=="Alpha" for x in data))

    def test_get_metadata(self):
        r = self.client.get("/media/Alpha")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data["author"], "A")

    def test_create_and_delete(self):
        new = {"name":"Gamma","publication_date":"2022-02-02","author":"C","category":"Magazine"}
        r = self.client.post("/media", json=new)
        self.assertEqual(r.status_code, 201)
        r = self.client.delete("/media/Gamma")
        self.assertEqual(r.status_code, 200)

if __name__=="__main__":
    unittest.main()
