from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bike = fields.Boolean()
    bike_manufacturer = fields.Char(string="Manufacturer")
    bike_model = fields.Char(string="Model")
    rental_days = fields.Integer(default=1)

    @api.constrains("rental_days")
    def _check_rental_days(self):
        for record in self:
            if record.is_bike and record.rental_days < 1:
                raise ValidationError(
                    _(
                        "Rental days must be bigger than 0."
                        "Product name: %(rec_name)s",
                        rec_name=record.name,
                    )
                )


class ProductProduct(models.Model):
    _inherit = "product.product"

    bike_rent_ids = fields.One2many("bike.rent", inverse_name="bike_id")
