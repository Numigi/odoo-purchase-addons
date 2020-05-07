# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMove(models.Model):

    _inherit = "stock.move"

    def _propagate_owner_from_purchase_order(self):
        purchase_order = self.purchase_line_id.order_id
        self.move_line_ids.write(
            {"owner_id": purchase_order.partner_id.commercial_partner_id.id}
        )

    @api.multi
    def _action_assign(self):
        res = super()._action_assign()
        moves_with_consignment = self.filtered(
            lambda m: m.purchase_line_id.product_id.consignment
        )
        for move in moves_with_consignment:
            move._propagate_owner_from_purchase_order()
        return res
