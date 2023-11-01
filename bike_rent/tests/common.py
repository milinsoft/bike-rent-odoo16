from datetime import datetime, timedelta

from odoo import Command
from odoo.tests import TransactionCase


class TestBikeRentCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.BikeRent = cls.env["bike.rent"]
        cls.Product = cls.env["product.product"]
        cls.partner_rich_bank = cls.ResPartner.create(
            [
                {
                    "name": "Rich Bank LLC",
                    "is_company": True,
                    "child_ids": [Command.create({"name": "Jan Kowalski"})],
                }
            ]
        )
        cls.partner_jan = cls.partner_rich_bank.child_ids

    @classmethod
    def create_rent(cls, delta_days, partner_id=False):
        return cls.BikeRent.create(
            [
                {
                    "partner_id": partner_id and partner_id.id,
                    "rent_start": (now := datetime.now()),
                    "rent_stop": now + timedelta(days=delta_days),
                }
            ]
        )

    @classmethod
    def create_rental_product(cls, values=None):
        if not values:
            values = {}
        values.setdefault("name", "Test Bike rental product")
        values.setdefault("type", "service")
        values.setdefault("is_bike", True)
        values.setdefault("rental_days", 0)
        return cls.Product.create(values)
