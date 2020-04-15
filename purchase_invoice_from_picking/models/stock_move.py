# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    supplier_invoice_line_ids = fields.One2many(
        'account.invoice.line', 'receipt_move_id',
    )
