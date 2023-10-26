from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bike = fields.Boolean()
    bike_manufacturer = fields.Char(string="Manufacturer")
    bike_model = fields.Char(string="Model")


class ProductProduct(models.Model):
    _inherit = "product.product"

    rent_ids = fields.One2many("bike.rent", inverse_name="bike_id")
