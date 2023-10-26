from datetime import timedelta

from odoo.exceptions import UserError, ValidationError

from .common import TestBikeRentCommon


class TestBikeRent(TestBikeRentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bike_rent_record = cls.create_rent(delta_days=1)

    def test_01_check_rent_stop_prior_rent_start(self):
        with self.assertRaisesRegex(
            UserError, "Rent Stop date cannot be prior to Rent Start!"
        ):
            self.bike_rent_record.rent_start += timedelta(days=10)

    def test_02_compute_number_of_days(self):
        self.bike_rent_record.rent_stop += timedelta(days=10)
        self.assertEqual(self.bike_rent_record.number_of_days, 11)

    def test_03_check_rent_price_not_negative(self):
        with self.assertRaisesRegex(ValidationError, "Price cannot be negative"):
            self.bike_rent_record.price = -10
