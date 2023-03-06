# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_sale_order_line_data(self, purchase_line, dest_company, sale_order):
        """
        Copy the description from purchase order line to the
        new sale order line.
        """
        new_line = super(PurchaseOrder, self)._prepare_sale_order_line_data(
            purchase_line, dest_company, sale_order
        )
        new_line["name"] = purchase_line.name
        return new_line
