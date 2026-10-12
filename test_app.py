import unittest

from db import db, ProductModel, create_product
from app import app


class ProductApiTest(unittest.TestCase):
    def setUp(self):
        db.init(":memory:")
        db.connect(reuse_if_open=True)
        db.create_tables([ProductModel])
        self.client = app.test_client()

    def tearDown(self):
        db.drop_tables([ProductModel])
        db.close()

    def test_get_products_returns_list(self):
        create_product("Sugar", 32)
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["name"], "Sugar")

    def test_get_missing_product_returns_404(self):
        response = self.client.get("/api/products/999")
        self.assertEqual(response.status_code, 404)

    def test_create_product(self):
        response = self.client.post("/api/products", json={"name": "Eggs", "price": 12})
        self.assertEqual(response.status_code, 201)
        self.assertIn("productId", response.get_json())
        