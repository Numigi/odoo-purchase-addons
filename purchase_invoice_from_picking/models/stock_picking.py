# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    receipt_invoiced = fields.Boolean(
        compute="_compute_receipt_invoiced", store=True, compute_sudo=True
    )
    receipt_partially_invoiced = fields.Boolean(
        compute="_compute_receipt_invoiced", store=True, compute_sudo=True
    )

    @api.depends("move_lines.receipt_invoiced")
    def _compute_receipt_invoiced(self):
        for picking in self:
            invoiced_moves = picking._get_invoiced_moves()
            uninvoiced_moves = picking.move_lines - invoiced_moves
            picking.receipt_invoiced = (
                True if invoiced_moves and not uninvoiced_moves else False
            )
            picking.receipt_partially_invoiced = (
                True if invoiced_moves and uninvoiced_moves else False
            )

    def _get_invoiced_moves(self):
        return self.move_lines.filtered(lambda m: m.receipt_invoiced)
