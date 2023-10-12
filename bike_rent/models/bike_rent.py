from odoo import fields, models


class BikeRent(models.Model):
    _name = 'bike.rent'
    _description = 'Bike Rent'

    bike_name = fields.Char()
    customer_name = fields.Char()
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(currency_id=currency_id)
    rent_start = fields.Datetime()
    rent_stop = fields.Datetime()
    notes = fields.Text()
