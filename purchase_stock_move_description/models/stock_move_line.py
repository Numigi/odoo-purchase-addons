# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    purchase_description = fields.Text(
        related='move_id.purchase_line_id.name', string='Description',
        store=False, readonly=True)
