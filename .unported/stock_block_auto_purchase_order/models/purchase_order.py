# © 2018 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields
from odoo.addons.purchase.models.purchase import PurchaseOrder

BLOCK_AUTO_HELP = (
    "When checked, this field prevents products from being automatically added "
    "to the PO by the system."
)


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    block_auto_purchase_order = fields.Boolean(
        string="Block Automatic Product Add",
        default=False,
        states=PurchaseOrder.READONLY_STATES,
        help=BLOCK_AUTO_HELP,
    )

    @api.onchange("order_line")
    def onchange_lines_set_automatic_block(self):
        products = self.mapped("order_line.product_id")
        auto_block = products.filtered("block_auto_purchase_order")
        if auto_block:
            self.block_auto_purchase_order = True
