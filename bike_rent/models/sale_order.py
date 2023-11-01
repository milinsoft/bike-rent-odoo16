from datetime import timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bike_rent_ids = fields.One2many("bike.rent", "sale_order_id")

    def _create_bike_rentals(self):
        now = fields.Datetime.now()
        return self.env["bike.rent"].create(
            [
                {
                    "bike_id": line.product_id.id,
                    "partner_id": self.partner_id.id,
                    "price": line.price_total,
                    "rent_start": now,
                    "rent_stop": now + timedelta(days=line.product_id.rental_days),
                    "sale_order_line_id": line.id,
                }
                for line in self.order_line.filtered("product_id.is_bike")
            ]
        )

    def action_confirm(self):
        res = super().action_confirm()
        self._create_bike_rentals()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bike_rent_ids = fields.One2many("bike.rent", "sale_order_line_id")
