# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    @api.onchange("product_id", "location_id")
    def _automatically_set_consignment_owner(self):
        is_supplier_receipt = self.location_id.usage == "supplier"
        if self.product_id.consignment and is_supplier_receipt:
            self.owner_id = self.product_id.get_consignment_supplier()
