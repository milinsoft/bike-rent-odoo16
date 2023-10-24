from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_show_partner_rental(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "bike_rent.bike_rent_action"
        )
        action["domain"] = [
            (
                "partner_id",
                "in",
                [self.id, *(self.child_ids.mapped("id") if self.is_company else [])],
            )
        ]
        return action
