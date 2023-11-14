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
        cls.Website = cls.env["website"]
        cls.SaleOrder = cls.env["sale.order"]
        cls.SaleOrderLine = cls.env["sale.order.line"]
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
    def create_rent(cls, start_delta=-1, stop_delta=2, partner_id=False):
        """Create a new bike rental record.

        Args:
            start_delta (int, optional):
                The number of days to adjust the rental start date.
                If negative, the rental starts before the current date;
                otherwise, it starts in the future.
                Default is -1 (yesterday).
            stop_delta (int, optional):
                The number of days to adjust the rental stop date.
                Default is 2, indicating a two-days rental ending tomorrow.
            partner_id (record, optional):
                The partner associated with the rental. Default is False.

        Returns:
            record: The newly created 'bike.rent' record.

        """
        rent_start = datetime.now() + timedelta(days=start_delta)
        return cls.BikeRent.create(
            [
                {
                    "partner_id": partner_id and partner_id.id,
                    "rent_start": rent_start,
                    "rent_stop": rent_start + timedelta(days=stop_delta),
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
        return cls.Product.create(values)
