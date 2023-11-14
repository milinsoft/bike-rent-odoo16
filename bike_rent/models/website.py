from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _product_domain(self):
        res = super()._product_domain()
        res.append(("is_bike", "=", True))
        return res
