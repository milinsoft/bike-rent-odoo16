from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    bike_rent_ids = fields.One2many("bike.rent", "partner_id")
    rent_count = fields.Integer(compute="_compute_rent_count")

    @api.depends("bike_rent_ids", "child_ids")
    def _compute_rent_count(self):
        for record in self:
            record.rent_count = len(
                self.bike_rent_ids.ids + self.child_ids.bike_rent_ids.ids
            )

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
