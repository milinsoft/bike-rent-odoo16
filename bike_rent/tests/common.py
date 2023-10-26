from datetime import datetime, timedelta

from odoo.tests import TransactionCase


class TestBikeRentCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.BikeRent = cls.env["bike.rent"]

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
