# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockPicking(models.Model):

    _inherit = "stock.picking"

    purchase_user_id = fields.Many2one(
        related="move_lines.purchase_line_id.order_id.user_id",
        store=True,
    )
