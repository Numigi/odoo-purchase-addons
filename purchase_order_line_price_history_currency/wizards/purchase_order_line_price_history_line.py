# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseOrderLinePriceHistoryLine(models.TransientModel):

    _inherit = "purchase.order.line.price.history.line"

    currency_id = fields.Many2one(
        "res.currency", related="purchase_order_line_id.currency_id")
