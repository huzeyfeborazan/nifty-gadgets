from django.test import TestCase
from .models import Product

class ProductTests(TestCase):
    def setUp(self):
        Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=99.99,
            stock=10
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.stock, 10)
