# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_highest_parent_id = fields.Many2one(
        "res.partner",
        string="Parent company",
        related="partner_id.highest_parent_id",
        store=True,
    )
