from .common import TestBikeRentCommon


class TestWebsiteProducts(TestBikeRentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_website = cls.Website.create([{"name": "Test website"}])

    def test_01_sale_product_domain(self):
        products_domain = self.test_website.sale_product_domain()
        self.assertIn(
            ("is_bike", "=", True),
            products_domain,
            "ia_bike domain is not found in 'products_domain'",
        )
