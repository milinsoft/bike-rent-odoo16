from odoo.exceptions import ValidationError

from .common import TestBikeRentCommon


class TestRentalProduct(TestBikeRentCommon):
    def test_01_check_rental_days_incorrect_values(self):
        expected_err_msg = "Rental days must be bigger than 0"

        with self.assertRaisesRegex(ValidationError, expected_err_msg):
            self.create_rental_product()

        with self.assertRaisesRegex(ValidationError, expected_err_msg):
            self.create_rental_product({"rental_days": -1})

    def test_02_check_rental_days_incorrect_values(self):
        rental = self.create_rental_product({"rental_days": 1})
        self.assertEqual(rental.rental_days, 1)

    def test_03_check_rental_days_on_regular_product(self):
        rental = self.create_rental_product({"is_bike": False})
        self.assertEqual(rental.rental_days, 0)

        rental = self.create_rental_product({"is_bike": False, "rental_days": -1})
        self.assertEqual(rental.rental_days, -1)

        rental = self.create_rental_product({"is_bike": False, "rental_days": 1})
        self.assertEqual(rental.rental_days, 1)
