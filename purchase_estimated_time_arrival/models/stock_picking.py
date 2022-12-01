# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()

        purchase_receipt_moves = self.mapped('move_lines').filtered(
            lambda m: m.purchase_line_id and m.location_id.usage == 'supplier'
        )

        for line in purchase_receipt_moves:
            line.sudo()._generate_arrival_time_entry()

        return res


class StockMove(models.Model):

    _inherit = "stock.move"

    def _generate_arrival_time_entry(self):
        self.env['stock.arrival.time'].create({
            'move_id': self.id,
            'product_id': self.product_id.id,
            'purchase_date': self.purchase_line_id.order_id.date_order,
            'receipt_date': self.date,
        })
