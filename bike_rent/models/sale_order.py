from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
                    "rent_stop": now + timedelta(days=line.bike_rent_days),
                    "sale_order_line_id": line.id,
                }
                for line in self.order_line.filtered("product_is_bike")
            ]
        )

    def action_confirm(self):
        res = super().action_confirm()
        self._create_bike_rentals()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bike_rent_ids = fields.One2many("bike.rent", "sale_order_line_id")
    product_is_bike = fields.Boolean(related="product_id.is_bike")
    bike_rent_days = fields.Integer(
        string="Rental Days",
        compute="_compute_bike_rent_days",
        inverse="_inverse_bike_rent_days",
    )

    @api.depends("product_uom_qty")
    def _compute_bike_rent_days(self):
        for record in self:
            record.bike_rent_days = record.product_uom_qty

    def _inverse_bike_rent_days(self):
        for record in self:
            record.product_uom_qty = record.bike_rent_days

    @api.constrains("bike_rent_days")
    def _check_bike_rent_days(self):
        for record in self:
            if record.product_is_bike and record.bike_rent_days < 1:
                raise ValidationError(
                    _(
                        "Rental days must be greater than 0"
                        "Product name: %(rec_name)s",
                        rec_name=record.name,
                    )
                )

    @api.onchange("bike_rent_days")
    def _onchange_bike_rent_days(self):
        # Since bike_rent_days is just a related field - sync is done on save,
        # this method will ensure smooth visual updates
        for record in self:
            record.product_uom_qty = record.bike_rent_days
