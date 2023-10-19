from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class BikeRent(models.Model):
    _name = "bike.rent"
    _description = "Bike Rent"

    bike_id = fields.Many2one("product.product")
    customer_id = fields.Many2one("res.partner")
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    price = fields.Monetary(currency_id=currency_id)
    rent_start = fields.Datetime(required=True)
    rent_stop = fields.Datetime(required=True)
    notes = fields.Text()
    number_of_days = fields.Integer(compute="_compute_number_of_days", default=0)

    @api.depends("rent_start", "rent_stop")
    def _compute_number_of_days(self):
        for record in self.filtered(lambda r: r.rent_start and r.rent_stop):
            record.number_of_days = (record.rent_stop - record.rent_start).days

    @api.constrains("rent_start", "rent_stop")
    def _check_rent_stop_prior_rent_start(self):
        for record in self.filtered(lambda r: r.rent_stop < r.rent_start):
            raise UserError(
                _(
                    "Rent Stop date cannot be prior to Rent Start!"
                    "Bike Rent ID: #%(rec_id)s",
                    rec_id=record.id,
                )
            )

    @api.constrains("price")
    def _check_rent_price_not_negative(self):
        for record in self.filtered(
            lambda r: r.currency_id.compare_amounts(r.price, 0) == -1
        ):
            raise ValidationError(
                _(
                    "Price cannot be negative. Bike Rent ID: #%(rec_id)s, "
                    "price %(curr)s%(price)s",
                    rec_id=record.id,
                    curr=record.currency_id.symbol,
                    price=record.price,
                )
            )
