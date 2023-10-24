from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bike = fields.Boolean()
    bike_manufacturer = fields.Char(string="Manufacturer")
    bike_model = fields.Char(string="Model")
