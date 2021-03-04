# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    supplier_invoice_line_ids = fields.One2many(
        "account.invoice.line", "receipt_move_id"
    )

    receipt_invoiced = fields.Boolean(
        compute="_compute_receipt_invoiced", store=True, compute_sudo=True
    )

    @api.depends(
        "supplier_invoice_line_ids", "supplier_invoice_line_ids.invoice_id.state"
    )
    def _compute_receipt_invoiced(self):
        for move in self:
            non_cancelled_invoice_lines = move.supplier_invoice_line_ids.filtered(
                lambda l: l.invoice_id.state != "cancel"
            )
            move.receipt_invoiced = bool(non_cancelled_invoice_lines)
