from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import Form

from .common import TestBikeRentCommon

DISCREPANCY_ERR_MSG = "bike_rent_days is not equal to product_uom_qty"
INVALID_VALUE_MSG = "Rental days must be greater than 0."


class TestBikeSaleOrderLine(TestBikeRentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bike_product = cls.create_rental_product()
        cls.sale_1 = cls.SaleOrder.create(
            {
                "partner_id": cls.partner_rich_bank.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.bike_product.id,
                            "name": "Test Bike rental product",
                            "product_uom_qty": 1.0,
                            "price_unit": cls.bike_product.lst_price,
                        }
                    )
                ],
            }
        )
        cls.sale_1_lines = cls.sale_1.order_line

    def test_01_so_created_with_one_order_line(self):
        self.assertEqual(
            len(self.sale_1_lines), 1, "incorrect number of sale order lines"
        )

    def test_02_product_is_bike_flag(self):
        self.assertTrue(
            self.sale_1_lines.product_is_bike
        ), "Incorrect 'product_is_bike' value"

    def test_03_bike_rent_days_equal_product_uom_qty(self):
        self.assertEqual(
            self.sale_1_lines.bike_rent_days,
            self.sale_1_lines.product_uom_qty,
            DISCREPANCY_ERR_MSG,
        )

    def test_04_bike_rent_days_equal_product_uom_qty(self):
        # WHEN
        self.sale_1_lines.bike_rent_days += 1
        # THEN
        self.assertEqual(
            self.sale_1_lines.bike_rent_days,
            self.sale_1_lines.product_uom_qty,
            DISCREPANCY_ERR_MSG,
        )
        # WHEN
        self.sale_1_lines.product_uom_qty += 1
        # THEN
        self.assertEqual(
            self.sale_1_lines.bike_rent_days,
            self.sale_1_lines.product_uom_qty,
            DISCREPANCY_ERR_MSG,
        )

    def test_05_check_bike_rent_days_is_positive(self):
        with self.assertRaisesRegex(ValidationError, INVALID_VALUE_MSG):
            self.sale_1_lines.bike_rent_days = -20

        with self.assertRaisesRegex(ValidationError, INVALID_VALUE_MSG):
            self.sale_1_lines.bike_rent_days = 0

    def test_06_onchange_bike_rent_days(self):
        so_form = Form(self.sale_1)
        with so_form.order_line.edit(0) as line:
            line.bike_rent_days += 10
            self.assertEqual(
                line.bike_rent_days,
                line.product_uom_qty,
                "Onchange method doesn't work",
            )

    def test_07_onchange_bike_rent_days_disabled(self):
        self.SaleOrderLine._onchange_methods.pop("bike_rent_days")

        so_form = Form(self.sale_1)
        with so_form.order_line.edit(0) as line:
            line.bike_rent_days += 10
            self.assertNotEqual(
                line.bike_rent_days,
                line.product_uom_qty,
                "Incorrect product_uom_qty value (without onchange method)",
            )
