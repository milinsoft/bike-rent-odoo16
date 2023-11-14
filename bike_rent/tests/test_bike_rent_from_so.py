from datetime import timedelta

from odoo import Command

from .common import TestBikeRentCommon

RENTAL_PERIODS = (1, 3, 5, 7)
LEN_RENTAL_PERIODS = len(RENTAL_PERIODS)


class TestBikeRentFromSO(TestBikeRentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.SaleOrder = cls.env["sale.order"]
        cls.so_bike_rentals = cls.SaleOrder.create(
            [
                {
                    "partner_id": cls.partner_rich_bank.id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": cls.create_rental_product().id,
                                "bike_rent_days": bike_rent_days,
                                "price_unit": 5,
                            }
                        )
                        for bike_rent_days in RENTAL_PERIODS
                    ],
                }
            ]
        )

    def test_01_test_order_lines_number(self):
        self.assertEqual(len(self.so_bike_rentals.order_line), LEN_RENTAL_PERIODS)

    def test_02_bike_rent_ids_is_not_yet_created(self):
        self.assertFalse(self.so_bike_rentals.bike_rent_ids)

    def test_03_test_create_rental_from_so(self):
        # WHEN
        self.so_bike_rentals.action_confirm()
        # THEN
        self.assertEqual(
            self.so_bike_rentals.bike_rent_ids,
            self.BikeRent.search([("sale_order_id", "=", self.so_bike_rentals.id)]),
        )
        self.assertEqual(
            tuple(self.so_bike_rentals.bike_rent_ids.mapped("number_of_days")),
            RENTAL_PERIODS,
        )

        for line in self.so_bike_rentals.order_line:
            rental = line.bike_rent_ids
            for value, expected_value in [
                (rental.partner_id, self.so_bike_rentals.partner_id),
                (rental.bike_id, line.product_id),
                (rental.currency_id.is_zero(rental.price - line.price_total), True),
                (rental.rent_start, self.so_bike_rentals.date_order),
                (
                    rental.rent_stop,
                    self.so_bike_rentals.date_order
                    + timedelta(days=line.bike_rent_days),
                ),
                (rental.number_of_days, line.bike_rent_days),
            ]:
                self.assertEqual(
                    value, expected_value, f"Wrong {value} Bike Rent #{rental.id}"
                )
